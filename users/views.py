from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from dishes.models import Basket
from users.models import User
from django.contrib.auth.views import LoginView
from users.forms import UserLoginForm, UserRegistrationForm
from django.views.generic.edit import CreateView
from common.views import TitleMixin
from django.contrib.messages.views import SuccessMessageMixin


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


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required()
def basket(request):
    baskets = Basket.objects.filter(user=request.user)
    total_sum = sum(basket.sum() for basket in baskets)
    total_quantity = sum(basket.quantity for basket in baskets)

    context = {
        'baskets': baskets,
        'total_sum': total_sum,
        'total_quantity': total_quantity,
    }
    return render(request, 'dishes/basket.html', context)


    