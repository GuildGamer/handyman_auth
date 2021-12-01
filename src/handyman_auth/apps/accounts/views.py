from django.http import response
from .serializers import UserModelSerializer
from django.db import transaction
from .models import HandyManBaseUser
from sentry_sdk import capture_exception
from rest_framework.response import Response
from rest_framework import viewsets, parsers, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.decorators import action
from django.db import transaction
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.authtoken.models import Token
from handyman_auth.settings import ACTIVATE_LINK_URL

from django.contrib.auth.tokens import default_token_generator

User = get_user_model()
activate_link_url = ACTIVATE_LINK_URL


class UserViewSet(viewsets.ModelViewSet):

    """
    HandyManUser Viewset
    """

    serializer_class = UserModelSerializer
    queryset = HandyManBaseUser.objects.all()
    permission_classes = [AllowAny]
    parser_classes = (parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser)

    @action(
        methods=[
            "POST",
        ],
        detail=False,
        url_path="sign-up",
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
            data = {"success": False, "error": True, "msg": sz.errors}

            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = sz.save()
            confirmation_token = default_token_generator.make_token(user)
            activation_link = f"{activate_link_url}?user_id={user.id}&confirmation_token={confirmation_token}"
            print(activation_link)
            # user.set_password(sz.data["password"])

            data = {
                "success": True,
                "data": {
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "firstname": user.firstname,
                        "lastname": user.lastname,
                        # "token":user.token
                    }
                },
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

        return Response(data=data, status=stats)

    @action(
        methods=[
            "POST",
        ],
        detail=False,
        url_path="sign-in",
        permission_classes=[AllowAny],
        parser_classes=(
            parsers.MultiPartParser,
            parsers.FormParser,
            parsers.JSONParser,
        ),
    )
    @transaction.atomic
    def sign_in(self, request):
        email = request.data["email"]
        password = request.data["password"]
        try:
            user: User = User.objects.filter(email=email).first()
        except User.DoesNotExist:
            return Response(
                {"error": True, "message": "Please check your username and password"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            capture_exception(e)
            print(e)
            return Response(
                {
                    "error": "unable to log you in at this moment, please try again later"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not user.check_password(password):
            return Response(
                {"error": "invalid credentials"}, status=status.HTTP_403_FORBIDDEN
            )
        if user.is_active == False:
            return Response(
                data={"verify email to activate account"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        with transaction.atomic():
            try:
                token = Token.objects.get(user=user)
                token.delete()

            except Token.DoesNotExist:
                pass

            token = user.create_token()
            user.token = token
            user.save()
            user.refresh_from_db()

        data = UserModelSerializer(user).data
        data["token"] = user.token
        data["timestamp"] = timezone.now().timestamp()

        response_data = {
            "success": True,
            "data": {
                "user": {
                    "id": data["id"],
                    "email": data["email"],
                    "firstname": data["firstname"],
                    "lastname": data["lastname"],
                    "phone": data["phone"],
                    "token": data["token"],
                    "timestamp": data["timestamp"],
                }
            },
        }

        return Response(data=response_data, status=status.HTTP_200_OK)

    @action(detail=False, permission_classes=[AllowAny], methods=["get"])
    def activate(self, request, id=None):
        user_id = request.query_params.get("user_id", "")
        confirmation_token = request.query_params.get("confirmation_token", "")
        try:
            user = self.get_queryset().get(id=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is None:
            return Response("User not found", status=status.HTTP_400_BAD_REQUEST)
        if not default_token_generator.check_token(user, confirmation_token):
            return Response(
                "Token is invalid or expired. Please request another confirmation email by signing in.",
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.email_confirmed = True
        user.is_active = True
        user.save()
        return Response("Email successfully confirmed")

        # sign-up including email verification for activation
        # delete account
        # deactivate account
        # logout
        # profile editing and change password
        # forgotten password
