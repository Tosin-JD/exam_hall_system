from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

class CustomUserManager(UserManager):
    pass

class CustomUser(AbstractUser):
    # Add any additional fields you need
    user_type = models.CharField(max_length=20)
    
    objects = CustomUserManager()

class Student(CustomUser):
    def save(self, *args, **kwargs):
        # Set is_staff to True when creating a new user
        if not self.pk:  # Check if the instance is being created
            self.is_staff = False
        super().save(*args, **kwargs)

class Invigilator(CustomUser):
    def save(self, *args, **kwargs):
        # Set is_staff to True when creating a new user
        if not self.pk:  # Check if the instance is being created
            self.is_staff = True
        super().save(*args, **kwargs)
