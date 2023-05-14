from django.urls import path, include
from rest_framework import routers

from api.views import DishModelViewSet, BasketModelViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'dishes', DishModelViewSet)
router.register(r'baskets', BasketModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

