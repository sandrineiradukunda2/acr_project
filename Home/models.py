from django.db import models
from django.utils import timezone

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Consider using Django's built-in authentication system
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    gender_choices = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=gender_choices)
    dob = models.DateTimeField(default=timezone.now)   

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
