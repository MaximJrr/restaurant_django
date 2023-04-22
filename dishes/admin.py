from django.contrib import admin

from dishes.models import Dish, DishCategory, Basket


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']
    search_fields = ['name']
    ordering = ['name']


@admin.register(DishCategory)
class DishAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    ordering = ['name']


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ['dish', 'quantity']
    extra = 0
