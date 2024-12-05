"""
Custom permissions for the API.
"""

from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from .models import Group


class IsCourseTeacher(BasePermission):
    """
    Custom permission to check if the user is the teacher of the course or the group.
    """

    def has_permission(self, request, view):
        """
        Check if the user has permission to perform the action.

        Args:
            request (HttpRequest): The HTTP request being processed.
            view (APIView): The view that is handling the request.

        Returns:
            bool: True if the user has permission, False otherwise.
        """
        user = request.user
        group_id = view.kwargs.get("group_id")

        if group_id:
            return Group.objects.filter(
                id=group_id, memberships__user=user, memberships__role="teacher"
            ).exists()

        return True

    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to modify the object.

        Args:
            request (HttpRequest): The HTTP request being processed.
            view (APIView): The view that is handling the request.
            obj (Model): The object that the permission check is against.

        Raises:
            PermissionDenied: If the user does not have permission to modify the object.

        Returns:
            bool: True if the user has permission, False otherwise.
        """
        user = request.user

        if hasattr(obj, "course") and obj.course.teacher == user:
            return True
        elif hasattr(obj, "teacher") and obj.teacher == user:
            return True
        raise PermissionDenied("You do not have permission to modify this object.")
