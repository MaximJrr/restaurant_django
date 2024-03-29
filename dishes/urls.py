from django.urls import path

from dishes.views import MenuView, CategoryListView, basket_add, basket_remove

app_name = 'dishes'

urlpatterns = [
    path('', MenuView.as_view(), name='menu'),
    path('category/<slug:category_slug>/', CategoryListView.as_view(), name='category'),
    path('page/<int:page>/', MenuView.as_view(), name='paginator'),
    path('add/<int:dish_id>/', basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
]
