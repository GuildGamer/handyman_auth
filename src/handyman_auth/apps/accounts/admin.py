from django.contrib import admin

from handyman_auth.apps.accounts.models import HandyManBaseUser

admin.site.register(HandyManBaseUser)
