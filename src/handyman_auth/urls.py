from django.contrib import admin
from django.urls import path, include
from .views import home

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path('sentry-debug/', trigger_error),
    path('', home, name="home"),
    path('admin/', admin.site.urls),
    path('api/', include("handyman_auth.apps.accounts.urls", namespace="accounts"))
]




