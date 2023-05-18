from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from common.views import TitleMixin
from users.forms import UserLoginForm, UserRegistrationForm, ReservationForm
from users.models import EmailVerification, User, Reservation


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Авторизация'


class UserRegisterView(TitleMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Регистрация прошла успешно'


class ReservationView(CreateView):
    model = Reservation
    template_name = 'users/reservation.html'
    form_class = ReservationForm
    success_url = reverse_lazy('dishes:index')

    def form_valid(self, form):
        return super().form_valid(form)


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        unique_code = kwargs['unique_code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, unique_code=unique_code)

        if email_verifications.exists() and not email_verifications.last().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required()
def basket(request):
    return render(request, 'dishes/basket.html')


# def reservation(request):
#     if request.method == 'POST':
#         form = ReservationForm(request.POST)
#         if form.is_valid():
#             client_name = form.cleaned_data['client_name']
#             number_of_quests = form.cleaned_data['number_of_quests']
#             date_and_time = form.cleaned_data['date_and_time']
#
#             reservation = Reservation(
#                 name=client_name,
#                 how_many_people=number_of_quests,
#                 date_time=date_and_time
#             )
#             reservation.save()
#             return redirect('users:email_verification')
#         else:
#             form = ReservationForm()
#     form = ReservationForm()
#     return render(request, 'users/reservation.html', {'form': form})

