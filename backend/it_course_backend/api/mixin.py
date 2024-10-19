"""
This module provides mixins for common functionality used in 
FAQ, Course, Group, Lesson, and Homework views.
It includes permission checks, logging of actions,
 and dynamic serializer selection based on user roles.
"""

import logging
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied

from .models import FAQ, Course, Group
from .serializers import (
    CourseSerializer,
    FAQSerializer,
    GroupCreateUpdateSerializer,
    TeacherCourseSerializer,
)

logger = logging.getLogger("api")


class FAQMixin:
    """
    Mixin for FAQ views, providing common functionality for listing and creating FAQs.
    """

    queryset = FAQ.active.all()
    serializer_class = FAQSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Save a new FAQ entry and log the action.
        """
        faq = serializer.save()
        logger.info("FAQ created: %s", faq.question)


class CourseMixin:
    """
    Mixin for course views, providing common functionality for managing courses,
    including selecting the serializer based on the user role.
    """

    queryset = Course.active.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        Select the appropriate serializer based on the user role.
        """
        if self.request.user.user_type == "teacher":
            return TeacherCourseSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        """
        Save a new course and log the action.
        """
        course = serializer.save()
        logger.info("Course created: %s", course.title)


class CoursePermissionMixin:
    """
    Mixin to enforce permissions for course modifications.
    Ensures only the teacher who created the course can modify it.
    """

    def get_object(self):
        """
        Retrieve the course object and verify that the requesting user is the teacher.
        """
        course = super().get_object()
        if course.teacher != self.request.user:
            raise PermissionDenied("You do not have permission to modify this course.")
        return course


class GroupMixin:
    """
    Mixin for group views, providing functionality for creating and managing groups.
    """

    queryset = Group.active.all()
    serializer_class = GroupCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Save a new group and log the action.
        """
        group = serializer.save()
        logger.info("Group created: %s", group.name)


class GroupPermissionMixin:
    """
    Mixin to enforce permissions for group modifications.
    Ensures only the teacher who created the group can modify it.
    """

    def get_object(self):
        """
        Retrieve the group object and verify that the requesting user is the teacher.
        """
        group = super().get_object()
        if group.teacher != self.request.user:
            raise PermissionDenied("You do not have permission to modify this group.")
        return group


class LessonPermissionMixin:
    """
    Mixin to enforce permissions for lesson modifications.
    Ensures only the teacher who created the lesson can modify it.
    """

    def get_object(self):
        """
        Retrieve the lesson object and verify that the requesting user is the teacher.
        """
        lesson = super().get_object()
        if lesson.course.teacher != self.request.user:
            raise PermissionDenied("You do not have permission to modify this lesson.")
        return lesson


class LessonActionMixin:
    """
    Mixin for logging actions related to lesson creation, updating, and deletion.
    """

    def perform_create(self, serializer):
        """
        Save a new lesson and log the action.
        """
        lesson = serializer.save()
        logger.info("Lesson created: %s", lesson.title)

    def perform_update(self, serializer):
        """
        Save the updated lesson and log the action.
        """
        lesson = serializer.save()
        logger.info("Lesson updated: %s", lesson.title)

    def perform_destroy(self, instance):
        """
        Delete the lesson and log the action.
        """
        logger.info("Lesson deleted: %s", instance.title)
        super().perform_destroy(instance)


class HomeworkActionMixin:
    """
    Mixin for logging actions related to homework creation, updating, and deletion.
    """

    def perform_create(self, serializer):
        """
        Save a new homework assignment and log the action.
        """
        homework = serializer.save()
        logger.info("Homework created: %s", homework.title)

    def perform_update(self, serializer):
        """
        Save the updated homework assignment and log the action.
        """
        homework = serializer.save()
        logger.info("Homework updated: %s", homework.title)

    def perform_destroy(self, instance):
        """
        Delete the homework assignment and log the action.
        """
        logger.info("Homework deleted: %s", instance.title)
        super().perform_destroy(instance)
