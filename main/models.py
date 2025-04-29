from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from rest_framework.views import APIView

from users.models import Account, Student


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField(validators=[MinValueValidator(0.0)])
    instructor = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.URLField(blank=True, null=True)
    video = models.FileField(upload_to='lessons/videos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user if self.user else 'Anonymous'}"


class Payment(models.Model):
    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'
    STATUS_CHOICES = (
        (PENDING, 'PENDING'),
        (COMPLETED, 'COMPLETED'),
        (FAILED, 'FAILED'),
    )
    user = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    amount = models.FloatField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=PENDING)
    payment_date = models.DateTimeField(auto_now_add=True)

    def is_paid(self):
        return self.status == self.COMPLETED

    def __str__(self):
        return f"Course: {self.course.title if self.course else 'N/A'}, To‘lovchi: {self.user if self.user else 'Noma’lum'}"



