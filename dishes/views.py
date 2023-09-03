from django.contrib.auth.decorators import login_required

from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.views.generic import ListView

from common.views import TitleMixin
from dishes.models import Basket, Dish, DishCategory


class IndexView(TitleMixin, ListView):
    active_section = 'index'
    template_name = 'dishes/index.html'
    title = 'Restaurant'
    model = Dish

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dishes'] = Dish.objects.all().order_by('-id')[:3]
        return context


class DishesListView(TitleMixin, ListView):
    active_section = 'menu'
    model = Dish
    template_name = 'dishes/menu.html'
    context_object_name = 'dishes'
    paginate_by = 4
    title = 'Restaurant - menu'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = DishCategory.objects.all()
        return context


def show_category(request, category_slug):
    dishes = Dish.objects.filter(category__slug=category_slug)
    categories = DishCategory.objects.all()

    context = {
        'dishes': dishes,
        'categories': categories,
    }

    return render(request, 'dishes/menu.html', context=context)


@login_required
def basket_add(request, dish_id):
    dish = Dish.objects.get(id=dish_id)
    Basket.add_or_update_basket(dish, request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def update_basket_quantity(request, basket_id):
    basket = get_object_or_404(Basket, id=basket_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        basket.quantity = quantity
        basket.total_price = int(basket.sum())
        basket.save()

        baskets = Basket.objects.filter(user=request.user)
        total_quantity = baskets.total_quantity()
        total_price_sum = int(baskets.total_sum())

        response_data = {
            'message': 'Количество блюд и итоговая цена успешно обновлены',
            'quantity': basket.quantity,
            'total_price_item': basket.total_price,
            'total_quantity': total_quantity,
            'total_price_sum': total_price_sum,
        }
        return JsonResponse(response_data)

    response_data = {'error': 'Произошла ошибка при обновлении количества блюд и итоговой цены'}
    return JsonResponse(response_data, status=400)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена!</h1>')



