from django.urls import path

from users.views import UserLoginView, UserRegisterView, logout, basket

app_name = 'users'

urlpatterns = [
    path('login', UserLoginView.as_view(), name='login'),
    path('register', UserRegisterView.as_view(), name='register'),
    path('logout', logout, name='logout'),
    path('basket', basket, name='basket')
]