import logging
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
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


class CourseListCreateView(generics.ListCreateAPIView):
    """
    API view to list and create courses with a role tag indicating if
    the user is a teacher or student in each course.
    """

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return courses where the user is a teacher or student.
        """
        user = self.request.user

        return Course.objects.filter(
            Q(teacher=user) | Q(group__students=user)
        ).distinct()

    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on user type.
        """
        return (
            TeacherCourseSerializer
            if self.request.user.user_type == "teacher"
            else CourseSerializer
        )

    def perform_create(self, serializer):
        """
        Save a new course entry, log its creation, and create a corresponding group.
        """
        course = serializer.save(teacher=self.request.user)
        logger.info("Course created: %s", course.title)

        group = Group.objects.create(
            name=f"{course.title} Group",
            teacher=self.request.user,
        )
        logger.info("Group created for course: %s", group.name)


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting a specific course with user role tag.
    """

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return a specific course based on the user's role.
        """
        user = self.request.user
        course_id = self.kwargs.get("pk")

        return Course.objects.filter(
            Q(id=course_id, teacher=user) | Q(id=course_id, group__students=user)
        ).distinct()


class CourseEditView(generics.UpdateAPIView):
    """
    API view for updating a specific course.

    Methods:
        PUT: Update an existing course entry.
    """

    permission_classes = [IsAuthenticated, IsCourseTeacher]

    def get_queryset(self):
        """
        Return a specific course for editing based on the user's role.

        Returns:
            QuerySet: A filtered queryset of the course for the authenticated user.
        """
        user = self.request.user
        course_id = self.kwargs.get("pk")
        if user.user_type == "teacher":
            return Course.objects.filter(id=course_id, teacher=user)
        return Course.objects.none()

    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on user type.

        Returns:
            Type: The serializer class for the current user.
        """
        return (
            TeacherCourseSerializer
            if self.request.user.user_type == "teacher"
            else CourseSerializer
        )


class GroupCreateView(generics.CreateAPIView):
    """
    API view to create a new group.

    Methods:
        POST: Create a new group entry.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = GroupCreateUpdateSerializer

    def perform_create(self, serializer):
        """
        Save a new group entry and log the creation.

        Args:
            serializer: The serializer instance containing the group data.
        """
        group = serializer.save(teacher=self.request.user)
        logger.info("Group created: %s", group.name)


class GroupEditView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting a specific group.

    Methods:
        GET: Retrieve a group entry by ID.
        PUT: Update an existing group entry.
        DELETE: Delete a specific group entry.
    """

    permission_classes = [IsAuthenticated, IsCourseTeacher]
    serializer_class = GroupCreateUpdateSerializer
    queryset = Group.objects.all()

    def perform_update(self, serializer):
        """
        Save the updated group entry and log the update.

        Args:
            serializer: The serializer instance containing the updated group data.
        """
        group = serializer.save()
        logger.info("Group updated: %s", group.name)

    def perform_destroy(self, instance):
        """
        Log the deletion of a group before destroying it.

        Args:
            instance: The group instance to be deleted.
        """
        logger.info("Group deleted: %s", instance.name)
        super().perform_destroy(instance)


class LessonListView(generics.ListAPIView):
    """
    View for listing lessons based on user role.

    Methods:
        GET: Retrieve a list of lessons for the authenticated user.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer

    def get_queryset(self):
        """
        Return lessons based on the user's role (teacher or student).

        Returns:
            QuerySet: A filtered queryset of lessons for the authenticated user.
        """
        user = self.request.user

        user_groups = Group.objects.filter(students=user).values_list("id", flat=True)

        if user.user_type == "teacher":
            return Lesson.objects.filter(course__teacher=user)
        elif user.user_type == "student":
            return Lesson.objects.filter(course__group__id__in=user_groups)

        return Lesson.objects.none()


class LessonCreateView(generics.CreateAPIView):
    """
    View for creating lessons.

    Methods:
        POST: Create a new lesson entry.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def perform_create(self, serializer):
        """
        Save a new lesson entry and log the creation.

        Args:
            serializer: The serializer instance containing the lesson data.
        """
        lesson = serializer.save()
        logger.info("Lesson created: %s", lesson.title)


class LessonEditView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, or deleting a specific lesson.

    Methods:
        GET: Retrieve a lesson entry by ID.
        PUT: Update an existing lesson entry.
        DELETE: Delete a specific lesson entry.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def perform_update(self, serializer):
        """
        Save the updated lesson entry and log the update.

        Args:
            serializer: The serializer instance containing the updated lesson data.
        """
        lesson = serializer.save()
        logger.info("Lesson updated: %s", lesson.title)

    def perform_destroy(self, instance):
        """
        Log the deletion of a lesson before destroying it.

        Args:
            instance: The lesson instance to be deleted.
        """
        logger.info("Lesson deleted: %s", instance.title)
        super().perform_destroy(instance)


class HomeworkListCreateView(generics.ListCreateAPIView):
    """
    View for listing and creating homework assignments.

    Methods:
        GET: Retrieve a list of homework assignments.
        POST: Create a new homework assignment.
    """

    permission_classes = [IsAuthenticated]
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer

    def perform_create(self, serializer):
        """
        Save a new homework assignment and log the creation.

        Args:
            serializer: The serializer instance containing the homework data.
        """
        homework = serializer.save()
        logger.info("Homework created: %s", homework.title)


class HomeworkDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, or deleting a specific homework assignment.

    Methods:
        GET: Retrieve a homework assignment by ID.
        PUT: Update an existing homework assignment.
        DELETE: Delete a specific homework assignment.
    """

    permission_classes = [IsAuthenticated]
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer


class HomeworkSubmissionView(generics.CreateAPIView):
    """
    View for submitting homework assignments.

    Methods:
        POST: Create a new homework submission.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = HomeworkSubmissionSerializer

    def perform_create(self, serializer):
        """
        Save a new homework submission and log the submission.

        Args:
            serializer: The serializer instance containing the submission data.
        """
        homework_submission = serializer.save(student=self.request.user)
        logger.info("Homework submitted by: %s", homework_submission.student.username)


class HomeworkGradeView(generics.UpdateAPIView):
    """
    View for grading homework submissions.

    Methods:
        PUT: Update the grade for a specific homework submission.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = HomeworkGradeSerializer
    queryset = Homework.objects.all()

    def perform_update(self, serializer):
        """
        Save the updated homework grade and log the grading.

        Args:
            serializer: The serializer instance containing the updated grade data.
        """
        homework = serializer.save()
        logger.info("Homework graded: %s", homework.title)


class LessonCalendarView(generics.ListAPIView):
    """
    View for displaying lessons in a calendar format.

    Methods:
        GET: Retrieve a list of lessons in a calendar format.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = LessonCalendarSerializer

    def get_queryset(self):
        """
        Return lessons for the current week based on user role.

        Returns:
            QuerySet: A filtered queryset of lessons for the authenticated user.
        """
        user = self.request.user
        start_date = timezone.now().date() - timezone.timedelta(
            days=timezone.now().date().weekday()
        )
        end_date = start_date + timezone.timedelta(days=7)

        user_courses = Course.objects.filter(students=user).values_list("id", flat=True)

        user_teaching_courses = Course.objects.filter(teacher=user).values_list(
            "id", flat=True
        )

        if user.user_type == "teacher":
            return Lesson.objects.filter(
                course__id__in=user_teaching_courses, date__range=(start_date, end_date)
            )

        elif user.user_type == "student":
            return Lesson.objects.filter(
                course__id__in=user_courses, date__range=(start_date, end_date)
            )

        return Lesson.objects.none()


class ReminderView(generics.ListAPIView):
    """
    View for listing homework reminders based on user type.

    Methods:
        GET: Retrieve a list of homework reminders for the authenticated user.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = HomeworkSerializer

    def get_queryset(self):
        """
        Return homework reminders based on the user's role.

        Returns:
            QuerySet: A filtered queryset of homework reminders for the authenticated user.
        """
        user = self.request.user
        now = timezone.now()

        if user.is_teacher:
            return Homework.objects.filter(
                lesson__course__groups__teacher=user,
                review_deadline__lte=now,
                submitted_by__isnull=False,
            )
        return Homework.objects.filter(
            lesson__course__groups__students=user,
            due_date__lte=now,
        )

    def list(self, request, *args, **kwargs):
        """
        List homework reminders and customize the response message based on user type.

        Args:
            request: The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A custom response containing the type of user and their reminders.
        """
        queryset = self.get_queryset()
        return {
            "type": "teacher" if request.user.is_teacher else "student",
            "message": (
                "You have homeworks to review"
                if request.user.is_teacher
                else "You have homeworks to submit"
            ),
            "data": self.get_serializer(queryset, many=True).data,
        }
