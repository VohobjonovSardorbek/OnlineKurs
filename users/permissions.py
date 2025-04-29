from rest_framework.permissions import BasePermission


class Is_Student(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role.lower() == 'student'


class Is_Teacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role.lower() == 'teacher'
