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
        """_summary_

        Args:
            request (_type_): _description_
            view (_type_): _description_
            obj (_type_): _description_

        Raises:
            PermissionDenied: _description_

        Returns:
            _type_: _description_
        """
        if hasattr(obj, 'course') and obj.course.teacher == request.user:
            return True
        raise PermissionDenied("You do not have permission to modify this object.")
