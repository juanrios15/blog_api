from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    birthday = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
