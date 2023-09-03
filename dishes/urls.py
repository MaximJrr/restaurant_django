from django.urls import path

from dishes.views import DishesListView, CategoryListView, basket_add, basket_remove

app_name = 'dishes'

urlpatterns = [
    path('', DishesListView.as_view(), name='index'),
    path('category/<slug:category_slug>/', CategoryListView.as_view(), name='category'),
    path('page/<int:page>/', DishesListView.as_view(), name='paginator'),
    path('add/<int:dish_id>/', basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
]
