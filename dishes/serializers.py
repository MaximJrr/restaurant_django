from rest_framework import serializers
from rest_framework import fields
from dishes.models import Dish, DishCategory, Basket


class DishSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=DishCategory.objects.all())

    class Meta:
        model = Dish
        fields = ['id', 'name', 'description', 'price', 'weight', 'image', 'category']


class BasketSerializer(serializers.ModelSerializer):
    dish = DishSerializer()
    sum = fields.FloatField(required=False)
    total_sum = fields.SerializerMethodField()
    total_quantity = fields.SerializerMethodField()

    class Meta:
        model = Basket
        fields = ['id', 'dish', 'sum', 'total_sum', 'total_quantity', 'quantity']

    def get_total_sum(self, obj):
        return Basket.objects.filter(user_id=obj.user.id).total_sum()

    def get_total_quantity(self, obj):
        return Basket.objects.filter(user_id=obj.user.id).total_quantity()








