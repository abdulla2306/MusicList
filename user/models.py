from datetime import timezone, timedelta
from random import random

from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    VIEWER = 'viewer', 'Viewer'
    EDITOR = 'editor', 'Editor'
    ADMIN = 'admin', 'Admin'
class CustomUser(AbstractUser):
    role = models.CharField(max_length=100, choices=Role, default=Role.VIEWER)
    email = models.EmailField(max_length=100,  blank=True, null=True)
    def __str__(self):
        return self.username

is_deleted = models.BooleanField(default=False)

def get_code():
    return random.randint(1000, 9999)

def checking_time():
    return timezone.now()+timedelta(minutes=1)

class Code(models.Model):
    code = models.CharField(max_length=6, default=get_code, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    expire_date = models.DateTimeField(default=checking_time)



from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid
User = get_user_model()
class PasswordResetRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() < self.created_at + timezone.timedelta(minutes=2)

    def str(self):
        return f'{self.user.username} - {self.code}'