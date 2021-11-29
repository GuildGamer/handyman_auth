from django.http import response
from .serializers import UserModelSerializer
from django.db import transaction
from .models import HandyManBaseUser
from sentry_sdk import capture_exception
from rest_framework.response import Response
from rest_framework import viewsets, parsers, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.decorators import action

class UserViewSet(viewsets.ModelViewSet):

    """
    HandyManUser Viewset
    """

    serializer_class = UserModelSerializer
    queryset = HandyManBaseUser.objects.all()
    permission_classes = [AllowAny]
    parser_classes = (parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser)

    @action(
        methods=["POST",],
        detail=False,
        url_path="create-account",
        permission_classes=[AllowAny],
        parser_classes=(
            parsers.MultiPartParser,
            parsers.FormParser,
            parsers.JSONParser,
        ),
    )
    @transaction.atomic
    def create_user(self, request):

        """
        view to create a new user
        """
        sz = UserModelSerializer(data=request.data)
        if not sz.is_valid():
            data = {
                "success": False,
                "error": True,
                "msg": sz.errors
            }

            return Response(data=data, status = status.HTTP_400_BAD_REQUEST)
        try:
            user = sz.save()
            user.set_password(sz.data["password"])
            
            data = {
                "success": True, 
                "data":{"user":{
                    "id": user.id,
                    "email": user.email,
                    "firstname": user.firstname,
                    "lastname": user.lastname,
                    "token":user.token
                }}
            }

            stats = status.HTTP_201_CREATED

        except Exception as e:
            capture_exception(e)
            print(e)

            data = {
                "success": False,
                "error": True,
                "msg": "Sorry, we are having trouble creatig your account at this time, try agian later",
            }

            stats = status.HTTP_200_OK
        
        return Response(data=data, status = stats)