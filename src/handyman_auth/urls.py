from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("handyman_auth.apps.accounts.urls", namespace="accounts"))
]
