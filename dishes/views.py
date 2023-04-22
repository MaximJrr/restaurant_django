from django.shortcuts import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView
from dishes.models import Dish, Basket
from common.views import TitleMixin


class IndexView(TitleMixin, TemplateView):
    template_name = 'dishes/index.html'
    title = 'Restaurant'


class DishesListView(TitleMixin, ListView):
    model = Dish
    template_name = 'dishes/menu.html'
    context_object_name = 'dishes'
    paginate_by = 1
    title = 'Restaurant - menu'

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(DishesListView, self).get_context_data()
    #     context['title'] = 'Menu'
    #     return context


@login_required
def basket_add(request, dish_id):
    dish = Dish.objects.get(id=dish_id)
    baskets = Basket.objects.filter(user=request.user, dish=dish)

    if not baskets.exists():
        Basket.objects.create(user=request.user, dish=dish, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

