from django.contrib import admin
from django.utils import timezone

from dishes.admin import BasketAdmin
from users.models import EmailVerification, User, Reservation


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'email', 'is_verified_email',
                    'check_is_verified_email', 'image'
    ]
    list_editable = ['username', 'first_name', 'last_name', 'is_verified_email']
    search_fields = ['username', 'first_name', 'last_ name', 'email']
    ordering = ['username']
    actions = ['delete_image']
    list_per_page = 10
    inlines = (BasketAdmin,)

    @admin.action(description="Удалить изображение у выбранных пользователей")
    def delete_image(self, request, queryset):
        queryset.update(image=None)

    @admin.display(description="Статус подтверждения почты")
    def check_is_verified_email(self, user: User):
        if user.is_verified_email:
            return 'Почта подтверждена'
        elif user.is_verified_email is False:
            return 'Почта не подтверждена'


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'unique_code', 'time_create', 'expiration_time']
    fields = ['user', 'unique_code', 'time_create', 'expiration_time']
    readonly_fields = ['time_create']


@admin.register(Reservation)
class VerificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'how_many_people', 'table_number', 'time_create', 'date_time', 'check_time']
    list_display_links = ['name']
    list_editable = ['how_many_people', 'table_number']
    ordering = ['time_create']
    readonly_fields = ['time_create']
    search_fields = ['name', 'date_time']
    list_per_page = 10

    @admin.display(description='Время до прибытия')
    def check_time(self, reservation: Reservation):
        current_time = timezone.now()
        return reservation.date_time - current_time

