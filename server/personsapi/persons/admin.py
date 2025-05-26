from django.contrib import admin
from .models import UserRole

from rest_framework.authtoken.models import Token

admin.site.register(Token)
