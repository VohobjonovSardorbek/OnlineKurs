from rest_framework.permissions import BasePermission

from main.models import Payment


class IsTeacherOrIsPaid(BasePermission):
    def has_object_permission(self, request, view, obj):

        user = request.user

        if obj.course.instructor == user:
            return True

        if hasattr(user, 'student') and obj.course.instructor == user:
            return Payment.objects.filter(
                user=user.student,
                course=obj.course,
                status=Payment.COMPLETED
            ).exists()

        return False

