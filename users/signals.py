# users/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Account, Student

@receiver(post_save, sender=Account)
def create_student_profile(sender, instance, created, **kwargs):
    if created and instance.role.lower() == 'student':
        Student.objects.create(user=instance)
