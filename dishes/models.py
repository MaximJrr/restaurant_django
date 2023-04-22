from django.db import models
from users.models import User


class DishCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return f'{self.name} | {self.description}'

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'


class Dish(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=3)
    image = models.ImageField(upload_to='dishes_images')
    category = models.ForeignKey(to=DishCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

    def __str__(self):
        return f'Блюдо: {self.name} | Категория: {self.category.name}'


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    dish = models.ForeignKey(to=Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Корзина для {self.user} | Блюдо: {self.dish.name}'

    def sum(self):
        return self.dish.price * self.quantity
    
    class Meta:
        verbose_name = 'Корзину пользователей'
        verbose_name_plural = 'Корзина пользователей'





