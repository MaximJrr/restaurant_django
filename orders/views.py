import stripe
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from dishes.models import Basket
from orders.forms import OrderForm
from orders.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(TemplateView):
    template_name = 'orders/success.html'
    extra_context = {'title': "Спасибо за заказ!"}


class CancelTemplateView(TemplateView):
    template_name = 'orders/cancel.html'


class OrderListView(ListView):
    template_name = 'orders/orders.html'
    queryset = Order.objects.all()
    ordering = ['-created']
    extra_context = {'title': 'Заказы'}

    def get_queryset(self):
        query_set = super(OrderListView, self).get_queryset()
        return query_set.filter(initiator=self.request.user)


class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['title'] = f'Заказ № - {self.object.id}'
        return context


class OrderCreateView(CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order-create')
    extra_context = {'title': "Оформление заказа"}

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        response = super().form_valid(form)
        baskets = Basket.objects.filter(user=self.request.user)
        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.stripe_products(),
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order-success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order-cancel')),
        )
        return redirect(checkout_session.url)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET_KEY
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session_id = event['data']['object']['id']
        session = stripe.checkout.Session.retrieve(session_id, expand=['line_items'])
        if session:
            fulfill_order(session)

    return HttpResponse(status=200)


def fulfill_order(session):
    order_id = session.metadata.order_id
    try:
        order = Order.objects.get(id=order_id, status=Order.CREATED)
        baskets = Basket.objects.filter(user=order.initiator)
        order.status = Order.PAID
        order.update_after_pay(baskets)
        order.save()
        baskets.delete()
    except Order.DoesNotExist:
        pass
