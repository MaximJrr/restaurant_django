from django.contrib import admin

from dishes.models import Basket, Dish, DishCategory


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'weight', 'description', 'category', 'price_info']
    list_editable = ['name', 'price', 'weight', 'category']
    search_fields = ['name']
    ordering = ['id']
    list_per_page = 10
    prepopulated_fields = {'slug': ('name',)}
    actions = ['default_price']

    @admin.display(description='Стоимость')
    def price_info(self, dish: Dish):
        if dish.price < 500:
            return "Низкая цена"
        elif 500 < dish.price < 1000:
            return "Средняя цена"
        else:
            return 'Цена выше среднего'

    @admin.action(description="Установить цену 0")
    def default_price(self, request, queryset):
        queryset.update(price=0)


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
