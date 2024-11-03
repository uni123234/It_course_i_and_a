import logging
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound
from django.db.models import Q
from ..models import Course, Homework, Lesson, Group, User
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
    View for listing and creating courses.
    Users can view courses they are teaching or courses that are available to their groups.
    """

    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieve the list of courses for the authenticated user.
        Returns courses where the user is the teacher or a student in the groups associated with the courses.

        Returns:
            QuerySet: A queryset of Course objects for the authenticated user.
        """
        user = self.request.user
        return Course.objects.filter(
            Q(teacher=user) | Q(groups__students=user)
        ).distinct()

    def get_serializer_class(self):
        """
        Determine the serializer class to use based on the user type.
        If the user is a teacher, use the TeacherCourseSerializer;
        otherwise, use the default CourseSerializer.

        Returns:
            Serializer: The appropriate serializer class for the current user.
        """
        if self.request.user.user_type == "teacher":
            return TeacherCourseSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        """
        Handle the creation of a new course.
        Assigns the authenticated user as the teacher for the newly created course,
        creates a group if it doesn't exist, and adds the user to that group.

        Args:
            serializer (Serializer): The serializer instance used to validate and save the course data.

        Returns:
            Response: A response containing the created course details.
        """
        user = self.request.user
        course = serializer.save(teacher=user)
        group, _ = Group.objects.get_or_create(course=course, teacher=user)
        group.students.add(user)
        logger.info("Course created by %s: %s", user.email, course.title)
        return Response(
            {"id": course.id, "title": course.title, "description": course.description},
            status=status.HTTP_201_CREATED,
        )


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return all courses the user can access based on their role."""
        user = self.request.user

        if user.user_type == "teacher":
            return Course.objects.filter(teacher=user)
        elif user.user_type == "student":
            return Course.objects.filter(groups__students=user).distinct()
        return Course.objects.none()

    def get_object(self):
        """Retrieve the course if accessible by the user; otherwise, raise an access error."""
        course = super().get_object()
        user = self.request.user

        if user != course.teacher and not course.groups.filter(students=user).exists():
            raise PermissionDenied("You are not enrolled in this course.")

        return course

    def retrieve(self, request, *args, **kwargs):
        """Retrieve the course details along with user type information."""
        course = self.get_object()
        user = self.request.user

        is_teacher = user == course.teacher
        is_student = course.groups.filter(students=user).exists()

        serializer = self.get_serializer(course)
        return Response(
            {
                "course": serializer.data,
                "is_teacher": is_teacher,
                "is_student": is_student,
            }
        )


class CourseEditView(generics.UpdateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return a specific course for editing, with the first course at the start if applicable."""
        user = self.request.user
        course_id = self.kwargs.get("pk")

        queryset = (
            Course.objects.filter(id=course_id, teacher=user)
            if user.user_type == "teacher"
            else Course.objects.none()
        )

        first_course = Course.objects.first()
        if first_course and first_course not in queryset:
            queryset = Course.objects.filter(pk=first_course.pk) | queryset

        return queryset


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
        user = self.request.user
        user_groups = Group.objects.filter(students=user).values_list("id", flat=True)

        student_lessons = Lesson.objects.filter(course__groups__id__in=user_groups)
        teacher_lessons = Lesson.objects.filter(course__teacher=user)

        return student_lessons | teacher_lessons

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        for lesson in queryset:
            if lesson.course.teacher == request.user:
                lesson.user_role = "teacher"
            else:
                lesson.user_role = "student"

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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
    View for listing and creating homework assignments for a specific course.
    Methods:
        GET: Retrieve a list of all homework assignments for the specified course.
        POST: Create a new homework assignment for the specified course.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = HomeworkSerializer

    def get_queryset(self):
        course_id = self.request.query_params.get("course_id")
        user = self.request.user

        logger.info(f"User: {user}, Course ID: {course_id}")

        if course_id is None:
            logger.warning("No course_id provided in request.")
            return Homework.objects.none()

        # Filtering homeworks for the specified course
        queryset = Homework.objects.filter(
            lesson__course_id=course_id,
            lesson__course__is_active=True,  # Ensure the course is active
        ).distinct()

        logger.info(f"Retrieved queryset: {queryset}")
        return queryset

    def perform_create(self, serializer):
        """
        Save a new homework assignment and log the creation.
        Automatically associates the assignment with the course of the specified lesson.
        """
        lesson = serializer.validated_data.get("lesson")
        if lesson is None:
            logger.error("Lesson is required to create homework.")
            raise ValueError("Lesson is required to create homework.")

        homework = serializer.save(submitted_by=self.request.user, course=lesson.course)

        logger.info(
            "Homework created: %s for lesson %s and course %s",
            homework.title,
            homework.lesson_id,
            homework.course_id,
        )


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


class HomeworkEditView(generics.RetrieveUpdateAPIView):
    """
    View for editing homework assignments.

    Methods:
        GET: Retrieve a homework assignment by ID.
        PUT: Update an existing homework assignment.
    """

    permission_classes = [IsAuthenticated]
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer

    def perform_update(self, serializer):
        """
        Update a homework assignment and log the update.

        Args:
            serializer: The serializer instance containing the updated data.
        """
        homework = serializer.save()
        logger.info("Homework updated: %s", homework.title)


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
        Return lessons for the current month based on user role.

        Returns:
            QuerySet: A filtered queryset of lessons for the authenticated user.
        """
        user = self.request.user
        now = timezone.now()
        start_date = now.replace(day=1).date()
        end_date = now.replace(day=monthrange(now.year, now.month)[1]).date()

        user_courses = Course.objects.filter(student_groups__students=user).values_list(
            "id", flat=True
        )

        user_teaching_courses = Course.objects.filter(teacher=user).values_list(
            "id", flat=True
        )

        if user.user_type == "teacher":
            return Lesson.objects.filter(
                course__id__in=user_teaching_courses,
                scheduled_time__date__range=(start_date, end_date),
            )

        elif user.user_type == "student":
            return Lesson.objects.filter(
                course__id__in=user_courses,
                scheduled_time__date__range=(start_date, end_date),
            )

        return Lesson.objects.none()


class ReminderView(generics.ListAPIView):
    """
    View for listing all homework reminders across all courses based on user type.

    Methods:
        GET: Retrieve a list of all homework reminders for the authenticated user.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = HomeworkSerializer

    def get_queryset(self):
        """
        Return all homework reminders across all courses based on the user's role.

        Returns:
            QuerySet: A filtered queryset of homework reminders for the authenticated user.
        """
        user = self.request.user
        is_teacher = user.groups.filter(name="Teachers").exists()

        if is_teacher:
            return (
                Homework.objects.filter(submitted_by__isnull=False)
                .select_related("lesson", "lesson__course")
                .order_by("review_deadline")
            )
        else:
            return (
                Homework.objects.filter(lesson__course__groups__students=user)
                .select_related("lesson", "lesson__course")
                .order_by("due_date")
            )

    def list(self, request, *args, **kwargs):
        """
        List all homework reminders and customize the response message based on user type.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                "type": (
                    "teacher"
                    if request.user.groups.filter(name="Teachers").exists()
                    else "student"
                ),
                "message": (
                    "You have homeworks to review"
                    if request.user.groups.filter(name="Teachers").exists()
                    else "You have homeworks due soon"
                ),
                "data": serializer.data,
            }
        )
