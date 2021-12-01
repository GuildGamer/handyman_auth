from django.db import models

# from phone_field import PhoneField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from rest_framework.authtoken.models import Token
from .managers import HandyManBaseUserManager


class Country(models.Model):
    name = models.CharField(max_length=254)
    country_code = models.CharField(max_length=254)
    created = models.DateTimeField(auto_now_add=True)


class HandyManBaseUser(AbstractBaseUser, PermissionsMixin):
    GENDER = (
        ("m", "Male"),
        ("f", "Female"),
    )
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(max_length=254, unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    phone = models.CharField(max_length=36)
    created = models.DateTimeField(auto_now_add=True)
    email_confirmed = models.BooleanField(default=False)
    token = models.TextField(default="")
    firstname = models.CharField(max_length=254)
    lastname = models.CharField(max_length=254)
    dob = models.DateField("Date of Birth", null=True, blank=True)
    gender = models.CharField(choices=GENDER, max_length=1, blank=True, null=True)
    country = models.ForeignKey(
        "Country", verbose_name="country", on_delete=models.PROTECT, null=True
    )
    avatar = models.ImageField(upload_to="avatars/")

    objects = HandyManBaseUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def create_token(self):
        token = Token.objects.create(user=self)
        self.token = token
        return token.key


def HandyManSP(HandyManBaseUser):
    pass
