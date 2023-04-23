from django.contrib import admin

from dishes.admin import BasketAdmin
from users.models import EmailVerification, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'image']
    inlines = (BasketAdmin,)


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'unique_code', 'time_create', 'expiration_time']
    fields = ['user', 'unique_code', 'time_create', 'expiration_time']
    readonly_fields = ['time_create']
