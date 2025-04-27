from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_workstudy = models.BooleanField(default=False)
    default_password_used = models.BooleanField(default=True)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']  # Required for createsuperuser

    def __str__(self):
        return self.username
