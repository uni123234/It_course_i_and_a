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
    Mixin providing common functionality for FAQ views,
    including listing, creating, and logging FAQ entries.
    """

    queryset = FAQ.active.all()
    serializer_class = FAQSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Save a new FAQ entry and log the action.
        Logs the created FAQ's question.
        """
        faq = serializer.save()
        logger.info("FAQ created: %s", faq.question)


class CourseMixin:
    """
    Mixin for shared course functionality such as logging and role-based checks.
    """

    queryset = Course.active.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Save a new course and log the action.
        Checks if the user is a teacher and logs accordingly.
        """
        if self.request.user.user_type == "teacher":
            teacher_serializer = TeacherCourseSerializer(
                data=self.request.data, context={"request": self.request}
            )
            teacher_serializer.is_valid(raise_exception=True)
            course = teacher_serializer.save()
            logger.info("Course created by teacher: %s", course.title)
        else:
            course = serializer.save()
            logger.info("Course created: %s", course.title)


class CoursePermissionMixin:
    """
    Mixin to check if the current user is allowed to modify the course.
    Ensures only the teacher who created the course can edit or delete it.
    """

    def get_object(self):
        """
        Override to check if the user can modify the course.
        """
        course = super().get_object()
        if course.teacher != self.request.user:
            raise PermissionDenied("You do not have permission to modify this course.")
        return course


class GroupMixin:
    """
    Mixin for shared group functionality such as logging.
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
    Mixin to check if the current user is allowed to modify the group.
    Ensures only the teacher who created the group can edit or delete it.
    """

    def get_object(self):
        """
        Override to check if the user can modify the group.
        """
        group = super().get_object()
        if group.teacher != self.request.user:
            raise PermissionDenied("You do not have permission to modify this group.")
        return group


class LessonPermissionMixin:
    """
    Mixin to handle permission checks for lesson operations.
    """

    def get_object(self):
        """
        Override to check if the user can edit or delete the lesson.
        """
        lesson = super().get_object()
        if lesson.course.teacher != self.request.user:
            raise PermissionDenied("You do not have permission to modify this lesson.")
        return lesson


class LessonActionMixin:
    """
    Mixin to handle logging actions for lesson creation, updating, and deletion.
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
    Mixin to handle logging actions for homework assignments.
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
