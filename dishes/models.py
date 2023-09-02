import stripe
from django.conf import settings
from django.db import models
from django.urls import reverse

from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


class DishCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return f'{self.name} | {self.description}'

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('dishes:category', kwargs={'category_id': self.pk})


class Dish(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=3)
    weight = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='dishes_images', blank=True)
    category = models.ForeignKey(to=DishCategory, on_delete=models.CASCADE)
    stripe_price_id = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

    def __str__(self):
        return f'Блюдо: {self.name} | Категория: {self.category.name}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.stripe_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_price_id = stripe_product_price['id']
        super(Dish, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'], unit_amount=round(self.price * 100), currency='rub')
        return stripe_product_price


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)

    def stripe_products(self):
        line_items = []
        for basket in self:
            item = {
                'price': basket.dish.stripe_price_id,
                'quantity': basket.quantity,
            }
            line_items.append(item)
        return line_items


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    dish = models.ForeignKey(to=Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    objects = BasketQuerySet.as_manager()

    class Meta:
        verbose_name = 'Корзину пользователей'
        verbose_name_plural = 'Корзина пользователей'

    def __str__(self):
        return f'Корзина для {self.user} | Блюдо: {self.dish.name}'

    def sum(self):
        return self.dish.price * self.quantity

    def de_json(self):
        basket_item = {
            'dish_name': self.dish.name,
            'quantity': self.quantity,
            'price': float(self.dish.price),
            'sum': float(self.sum())
        }
        return basket_item

    @classmethod
    def add_or_update_basket(cls, dish_id, user):
        baskets = Basket.objects.filter(user=user, dish_id=dish_id)

        if not baskets.exists():
            obj = Basket.objects.create(user=user, dish=dish_id, quantity=1)
            is_created = True
        else:
            basket = baskets.first()
            basket.quantity += 1
            basket.save()
            is_created = False
            return basket, is_created




