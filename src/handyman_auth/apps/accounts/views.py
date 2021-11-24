from .serializers import UserModelSerializer
from .models import HandyManUser
from rest_framework import viewsets, parsers
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserModelSerializer
    queryset = HandyManUser.objects.all()
    permission_classes = [IsAuthenticated]
    parser_classes = (parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser)

    @action(
        methods=["POST",],
        detail=False,
        url_path="create-account",
        permission_classes=[IsAdminUser],
        parser_classes=(
            parsers.MultiPartParser,
            parsers.FormParser,
            parsers.JSONParser,
        ),
    )
    def create_user(request):
        pass