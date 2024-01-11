from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True, null=False)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "user_details"


class Login(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    login_time = models.DateTimeField(default=timezone.now)
    logout_time = models.DateTimeField()

    class Meta:
        db_table = "login_history"
