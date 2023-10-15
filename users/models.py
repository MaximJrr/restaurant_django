from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images')
    is_verified_email = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f'Пользователь: {self.username} | Email пользователя: {self.email}'


class EmailVerification(models.Model):
    unique_code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    time_create = models.DateTimeField(auto_now_add=True)
    expiration_time = models.DateTimeField()

    def __str__(self):
        return f'EmailVerification for {self.user.email}'

    def send_verification_email(self):
        link = reverse('users:email_verification', kwargs={'email': self.user.email, 'unique_code': self.unique_code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f"Подтверждение учетной записи для {self.user.username}"
        message = f"Для подтверждение учетной записи для {self.user.email} перейдите по ссылке {verification_link}"
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return True if now() >= self.expiration_time else False

    class Meta:
        verbose_name = 'Проверку электронной почты'
        verbose_name_plural = 'Проверка электронной почты'


class Reservation(models.Model):
    name = models.CharField(max_length=100)
    how_many_people = models.IntegerField(default=0)
    date_time = models.DateTimeField()
    time_create = models.DateTimeField(auto_now_add=True, null=True)
    table_number = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return f'Забронировал: {self.name} | Количество мест: {self.how_many_people} | Номер столика: {self.table_number} | Забронировано в: {self.time_create} | Дата и время: {self.date_time}'

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирование'
