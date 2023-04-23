from django.urls import path

from users.views import (EmailVerificationView, UserLoginView,
                         UserRegisterView, basket, logout)

app_name = 'users'

urlpatterns = [
    path('login', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('logout/', logout, name='logout'),
    path('basket', basket, name='basket'),
    path('email_verification/<str:email>/<uuid:unique_code>/', EmailVerificationView.as_view(), name='email_verification'),
]