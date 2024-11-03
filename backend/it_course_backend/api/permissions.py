"""
Custom permissions for the API.
"""
from rest_framework.permissions import BasePermission
from django.core.exceptions import PermissionDenied

class IsCourseTeacher(BasePermission):
    """
    Custom permission to check if the user is the teacher of the course related to the object.
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'course') and obj.course.teacher == request.user:
            return True
        raise PermissionDenied("You do not have permission to modify this object.")
