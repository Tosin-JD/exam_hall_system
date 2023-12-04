from django.contrib.auth.models import AbstractUser, UserManager, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True, blank=True)
    user_type = models.CharField(max_length=20)

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Student(CustomUser):
    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
        
    def save(self, *args, **kwargs):
        # Set is_staff to True when creating a new user
        if not self.pk:  # Check if the instance is being created
            self.is_staff = False
            self.user_type = "Student"
        super().save(*args, **kwargs)

class Invigilator(CustomUser):
    class Meta:
        verbose_name = 'Invigilator'
        verbose_name_plural = 'Invigilators'
        
    def save(self, *args, **kwargs):
        # Set is_staff to True when creating a new user
        if not self.pk:  # Check if the instance is being created
            self.is_staff = True
            self.user_type = "Invigilator"
        super().save(*args, **kwargs)
