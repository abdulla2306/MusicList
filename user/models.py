from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    VIEWER = 'viewer', 'Viewer'
    EDITOR = 'editor', 'Editor'
    ADMIN = 'admin', 'Admin'
class CustomUser(AbstractUser):
    role = models.CharField(max_length=1000, choices=Role, default=Role.VIEWER)

    def __str__(self):
        return self.username

is_deleted = models.BooleanField(default=False)