from django.urls import path

from dishes.views import DishesListView, basket_add, basket_remove, show_category

app_name = 'dishes'

urlpatterns = [
    path('', DishesListView.as_view(), name='index'),
    path('category/<slug:category_slug>/', show_category, name='category'),
    path('page/<int:page>/', DishesListView.as_view(), name='paginator'),
    path('add/<int:dish_id>/', basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
]
