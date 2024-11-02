import logging
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from ..models import Course, Homework, Lesson, Group
from ..serializers import (
    CourseSerializer,
    GroupCreateUpdateSerializer,
    TeacherCourseSerializer,
    LessonSerializer,
    HomeworkSerializer,
    HomeworkSubmissionSerializer,
    HomeworkGradeSerializer,
    LessonCalendarSerializer,
)
from ..permissions import IsCourseTeacher

logger = logging.getLogger("api")


class BaseListCreateView(generics.ListCreateAPIView):
    """Base view for listing and creating instances with user role checks."""

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Override this method to define the queryset for the view."""
        raise NotImplementedError("You must implement the get_queryset method.")


class CourseListCreateView(BaseListCreateView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        """Return courses where the user is involved as a teacher or student."""
        user = self.request.user
        return Course.objects.filter(
            Q(teacher=user) | Q(groups__students=user)
        ).distinct()

    def get_serializer_class(self):
        """Return the appropriate serializer based on user type."""
        return (
            TeacherCourseSerializer
            if self.request.user.user_type == "teacher"
            else CourseSerializer
        )

    def perform_create(self, serializer):
        """Save a new course and enroll the user as a student."""
        user = self.request.user
        course = serializer.save(teacher=user)
        group, _ = Group.objects.get_or_create(course=course, teacher=user)
        group.students.add(user)
        logger.info("Course created by %s: %s", user.email, course.title)


class BaseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Base view for retrieving, updating, or deleting instances with access checks."""

    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Retrieve the object if accessible by the user; otherwise, raise an access error."""
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj


class CourseDetailView(BaseRetrieveUpdateDestroyView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        """Return courses the user can access based on their role."""
        user = self.request.user
        if user.user_type == "teacher":
            return Course.objects.filter(teacher=user)
        elif user.user_type == "student":
            return Course.objects.filter(groups__students=user).distinct()
        return Course.objects.none()


class CourseEditView(generics.UpdateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return a specific course for editing if the user is the teacher."""
        user = self.request.user
        course_id = self.kwargs.get("pk")
        return Course.objects.filter(id=course_id, teacher=user)


class GroupCreateView(generics.CreateAPIView):
    """API view to create a new group."""

    permission_classes = [IsAuthenticated]
    serializer_class = GroupCreateUpdateSerializer

    def perform_create(self, serializer):
        """Save a new group entry and log the creation."""
        group = serializer.save(teacher=self.request.user)
        logger.info("Group created: %s", group.name)


class GroupEditView(BaseRetrieveUpdateDestroyView):
    """API view for retrieving, updating, or deleting a specific group."""

    permission_classes = [IsAuthenticated, IsCourseTeacher]
    serializer_class = GroupCreateUpdateSerializer
    queryset = Group.objects.all()

    def perform_update(self, serializer):
        """Log the updated group entry."""
        group = serializer.save()
        logger.info("Group updated: %s", group.name)

    def perform_destroy(self, instance):
        """Log the deletion of a group before destroying it."""
        logger.info("Group deleted: %s", instance.name)
        super().perform_destroy(instance)


class LessonListView(BaseListCreateView):
    """View for listing lessons based on user role."""

    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        user_groups = Group.objects.filter(students=user).values_list("id", flat=True)
        return Lesson.objects.filter(
            Q(course__groups__id__in=user_groups) | Q(course__teacher=user)
        ).distinct()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        for lesson in queryset:
            lesson.user_role = (
                "teacher" if lesson.course.teacher == request.user else "student"
            )

        return Response(serializer.data)


class LessonCreateView(generics.CreateAPIView):
    """View for creating lessons."""

    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        """Save a new lesson and log the creation."""
        lesson = serializer.save()
        logger.info("Lesson created: %s", lesson.title)


class LessonEditView(BaseRetrieveUpdateDestroyView):
    """View for retrieving, updating, or deleting a specific lesson."""

    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def perform_update(self, serializer):
        """Log the updated lesson entry."""
        lesson = serializer.save()
        logger.info("Lesson updated: %s", lesson.title)

    def perform_destroy(self, instance):
        """Log the deletion of a lesson before destroying it."""
        logger.info("Lesson deleted: %s", instance.title)
        super().perform_destroy(instance)


class StudentHomeworkListView(generics.ListAPIView):
    """View for listing all homework assignments submitted by a specific student."""

    permission_classes = [IsAuthenticated]
    serializer_class = HomeworkSerializer

    def get_queryset(self):
        user = self.request.user
        student_id = self.kwargs.get("student_id")
        return (
            Homework.objects.filter(submitted_by__id=student_id)
            if user.user_type == "teacher"
            else Homework.objects.none()
        )


class HomeworkListCreateView(BaseListCreateView):
    """View for listing and creating homework assignments for a specific course."""

    serializer_class = HomeworkSerializer

    def get_queryset(self):
        user = self.request.user
        now = timezone.now()
        course_id = self.kwargs.get("course_id")

        if user.user_type == "teacher":
            return Homework.objects.filter(
                lesson__course__id=course_id,
                submission_date__isnull=False,
                due_date__lte=now,
            ).distinct()
        elif user.user_type == "student":
            return Homework.objects.filter(
                lesson__course__id=course_id, due_date__gte=now, submitted_by=user
            ).distinct()
        return Homework.objects.none()

    def perform_create(self, serializer):
        """Save a new homework assignment and log the creation."""
        homework = serializer.save(submitted_by=self.request.user)
        logger.info("Homework created: %s", homework.title)


class HomeworkDetailView(BaseRetrieveUpdateDestroyView):
    """View for retrieving, updating, or deleting a specific homework assignment."""

    serializer_class = HomeworkSerializer
    queryset = Homework.objects.all()


class HomeworkEditView(generics.UpdateAPIView):
    """View for editing homework assignments."""

    permission_classes = [IsAuthenticated]
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer

    def perform_update(self, serializer):
        """Log the updated homework entry."""
        homework = serializer.save()
        logger.info("Homework updated: %s", homework.title)


class HomeworkSubmissionView(generics.CreateAPIView):
    """View for submitting homework assignments."""

    permission_classes = [IsAuthenticated]
    serializer_class = HomeworkSubmissionSerializer

    def perform_create(self, serializer):
        """Save a new homework submission and log the submission."""
        homework_submission = serializer.save(student=self.request.user)
        logger.info("Homework submitted by: %s", homework_submission.student.username)


class HomeworkGradeView(generics.UpdateAPIView):
    """View for grading homework submissions."""

    permission_classes = [IsAuthenticated]
    serializer_class = HomeworkGradeSerializer
    queryset = Homework.objects.all()

    def perform_update(self, serializer):
        """Log the grading of homework."""
        homework = serializer.save()
        logger.info("Homework graded: %s", homework.title)


class LessonCalendarView(generics.ListAPIView):
    """View for displaying lessons in a calendar format."""

    permission_classes = [IsAuthenticated]
    serializer_class = LessonCalendarSerializer

    def get_queryset(self):
        """Return lessons for the current week based on user role."""
        user = self.request.user
        start_date = timezone.now().date() - timezone.timedelta(
            days=timezone.now().date().weekday()
        )
        end_date = start_date + timezone.timedelta(days=7)

        if user.user_type == "teacher":
            return Lesson.objects.filter(
                course__teacher=user, date__range=(start_date, end_date)
            )
        elif user.user_type == "student":
            user_courses = Course.objects.filter(students=user).values_list(
                "id", flat=True
            )
            return Lesson.objects.filter(
                course__id__in=user_courses, date__range=(start_date, end_date)
            )
        return Lesson.objects.none()


class ReminderView(generics.ListAPIView):
    """View for listing homework reminders based on user type."""

    permission_classes = [IsAuthenticated]
    serializer_class = HomeworkSerializer

    def get_queryset(self):
        """Return homework reminders based on the user's role."""
        user = self.request.user
        now = timezone.now()

        if user.groups.filter(name="Teachers").exists():
            return Homework.objects.filter(
                lesson__course__groups__teacher=user,
                review_date__isnull=True,
                due_date__gte=now,
            )
        elif user.groups.filter(name="Students").exists():
            return Homework.objects.filter(
                submitted_by=user, due_date__gte=now, review_date__isnull=True
            )
        return Homework.objects.none()
