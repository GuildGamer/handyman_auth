from django.contrib import admin
from django.urls import path, include
from .views import home

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("api/", include("handyman_auth.apps.accounts.urls", namespace="accounts")),
]
