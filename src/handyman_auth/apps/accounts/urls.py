from django.http.response import HttpResponse
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import(
    UserViewSet
)

router = DefaultRouter()
router.register(r'accounts', UserViewSet, basename='accounts')

urlpatterns = router.urls
app_name = "accounts"



