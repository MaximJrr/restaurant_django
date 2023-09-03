from django.contrib import admin

from dishes.models import Basket, Dish, DishCategory


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'category']
    search_fields = ['name']
    ordering = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(DishCategory)
class DishCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    ordering = ['name']
    prepopulated_fields = {'slug': ('name',)}


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ['dish', 'quantity']
    extra = 0
