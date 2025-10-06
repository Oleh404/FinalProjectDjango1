from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    USER_TYPE_CHOICES = [
        ('renter', 'Renter'),
        ('landlord', 'Landlord'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='renter')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()
