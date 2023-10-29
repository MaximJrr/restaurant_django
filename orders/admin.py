from django.contrib import admin

from orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'created', 'status']
    search_fields = ['id', 'first_name', 'last_name', 'email']
    list_display_links = ['first_name', 'last_name']
    ordering = ['-created']
    list_editable = ['address', 'status']
    list_per_page = 10
    readonly_fields = ['id', 'created']
