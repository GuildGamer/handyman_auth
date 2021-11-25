from django.db import models
from phone_field import PhoneField
from django.contrib.auth.models import AbstractBaseUser
from rest_framework.authtoken.models import Token


class Country(models.Model):
    name = models.CharField(max_length=254)
    country_code = models.CharField(max_length=254)
    created = models.DateTimeField(auto_now_add=True)

class HandyManUser(AbstractBaseUser):

    GENDER = (
        ("m" , "Male"),
        ("f" , "Female"),
    )
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(max_length=254, unique=True)
    phone = PhoneField()
    created = models.DateTimeField(auto_now_add=True)
    email_confirmed = models.BooleanField(default=False)
    token = models.TextField(default = "")
    firstname = models.CharField(max_length=254)
    lastname = models.CharField(max_length=254)
    dob = models.DateField("Date of Birth", null=True, blank= True)
    gender = models.CharField(choices=GENDER, max_length=1)
    country = models.ForeignKey("Country", verbose_name="country", on_delete=models.PROTECT)
    avatar = models.ImageField(upload_to="avatars/")
    

    def create_token(self):
        token = Token.objects.create(user=self)
        self.token = token
        return token.key
    
