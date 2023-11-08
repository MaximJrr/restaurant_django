from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from users.forms import UserLoginForm, UserRegistrationForm, ReservationForm
from users.models import EmailVerification, User, Reservation


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    extra_context = {'title': "Авторизация"}


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Регистрация прошла успешно'
    extra_context = {'title': 'Регистрация'}


class ReservationView(LoginRequiredMixin, CreateView):
    model = Reservation
    template_name = 'users/reservation.html'
    form_class = ReservationForm
    success_url = reverse_lazy('users:reservation_verification')
    extra_context = {'title': 'Бронирование'}

    def form_valid(self, form):
        table_number = form.cleaned_data['table_number']
        date_time = form.cleaned_data['date_time']
        reservations = Reservation.objects.filter(date_time=date_time, table_number=table_number)

        if reservations.exists():
            message = "Данное место на указанное время уже занято, выберите другое место, или время"
            return render(self.request, self.template_name, {'form': form, 'message': message})
        else:
            return super().form_valid(form)


class ReservationVerificationView(TemplateView):
    template_name = 'users/reservation_verification.html'
    extra_context = {'title': "Вы успешно забронировали место!"}


class EmailVerificationView(TemplateView):
    title = 'Подтверждение электронной почты'
    template_name = 'users/email_verification.html'
    extra_context = {'title': "Ваша учетная запись успешно подтверждена!"}

    def get(self, request, *args, **kwargs):
        unique_code = kwargs['unique_code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, unique_code=unique_code)

        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))


class BasketView(TemplateView):
    template_name = 'dishes/basket.html'
    extra_context = {'title': 'Корзина'}


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
