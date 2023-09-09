from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from dishes.models import Dish, Basket
from dishes.serializers import DishSerializer, BasketSerializer


class DishModelViewSet(ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

    def get_permissions(self):
        if self.action in ('update', 'create', 'destroy'):
            self.permission_classes = (IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly)
        return super(DishModelViewSet, self).get_permissions()


class BasketModelViewSet(ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        queryset = super(BasketModelViewSet, self).get_queryset()
        return queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            dish_id = request.data['dish_id']
            dishes = Dish.objects.filter(id=dish_id)
            if not dishes.exists():
                return Response({'dish_id': 'Такого блюда не существует'}, status=status.HTTP_400_BAD_REQUEST)
            obj, is_created = Basket.add_or_update_basket(dish_id, self.request.user)
            status_code = status.HTTP_201_CREATED if is_created else status.HTTP_200_OK
            serializer = self.get_serializer(obj)
            return Response(serializer.data, status=status_code)
        except KeyError:
            return Response({'dish_id': 'Это поле обязательное'}, status=status.HTTP_400_BAD_REQUEST)
