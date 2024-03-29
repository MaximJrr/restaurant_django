from django.urls import path

from users.views import (EmailVerificationView, UserLoginView,
                         UserRegisterView, BasketView, logout, ReservationView, ReservationVerificationView, UserProfileView)

app_name = 'users'

urlpatterns = [
    path('login', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('logout/', logout, name='logout'),
    path('basket/', BasketView.as_view(), name='basket'),
    path('email_verification/<str:email>/<uuid:unique_code>/', EmailVerificationView.as_view(), name='email_verification'),
    path('reservation/', ReservationView.as_view(), name='reservation'),
    path('reservation_verification', ReservationVerificationView.as_view(), name='reservation_verification'),
    path('profile/', UserProfileView.as_view(), name='profile')
]
