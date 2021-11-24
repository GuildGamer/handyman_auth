from rest_framework.routers import DefaultRouter
from .views import(
    AccountsViewSet
)

router = DefaultRouter()
router.register(r'accounts', AccountsViewSet, basename='accounts')

app_name = "accounts"
urlpatterns = router.urls