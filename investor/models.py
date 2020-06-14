from django.contrib.auth.models import AbstractUser
from django.db import models


class Investor(AbstractUser):
    GENDER_CHOICES = (
        ('m', 'Male'),
        ('f', 'Female')
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=False)
    ipo_notification = models.BooleanField(default=False, blank=False)
