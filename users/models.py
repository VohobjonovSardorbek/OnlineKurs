from django.db import models
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):
    ROLE_CHOICES = (
        ('Teacher', 'Teacher'),
        ('Student', 'Student'),
    )
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default="Teacher")


class Student(models.Model):
    course = models.ManyToManyField('main.Course', blank=True)
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user and self.user.username:
            return self.user.username
        return "No user"



