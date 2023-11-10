from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views

from dishes.views import IndexView, update_basket_quantity, pageNotFound
from orders.views import stripe_webhook_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('menu/', include('dishes.urls', namespace='dishes')),
    path('users/', include('users.urls', namespace='users')),
    path('accounts/', include('allauth.urls')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('webhook/stripe/', stripe_webhook_view, name='stripe_webhook'),
    path('api/', include('api.urls', namespace='api')),
    path('api-token-auth/', views.obtain_auth_token),
    path('update_basket_quantity/<int:basket_id>/', update_basket_quantity, name='update_basket_quantity'),
]


if settings.DEBUG:
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = pageNotFound