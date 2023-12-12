from django.contrib.auth.models import AbstractUser, UserManager, BaseUserManager
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from PIL import Image


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
    user_type = models.CharField(max_length=20, verbose_name="User Type")
    slug = models.SlugField(unique=True, blank=True, null=True)

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)

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

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    avatar = models.ImageField(
        default='avatar.jpg', # default avatar
        upload_to='profile_avatars' # dir to store the image
    )

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        # save the profile first
        super().save(*args, **kwargs)

        # resize the image
        img = Image.open(self.avatar.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            # create a thumbnail
            img.thumbnail(output_size)
            # overwrite the larger image
            img.save(self.avatar.path)
