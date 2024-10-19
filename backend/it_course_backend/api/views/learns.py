import logging
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone

from ..models import FAQ, Course, Homework, Lesson
from ..serializers import (
    CourseSerializer,
    FAQSerializer,
    LessonCalendarSerializer,
    LessonSerializer,
    HomeworkSerializer,
    HomeworkSubmissionSerializer,
    HomeworkGradeSerializer,
)
from ..mixin import (
    CourseMixin,
    CoursePermissionMixin,
    FAQMixin,
    GroupMixin,
    GroupPermissionMixin,
    HomeworkActionMixin,
    LessonActionMixin,
    LessonPermissionMixin,
)

logger = logging.getLogger("api")


class FAQListView(generics.ListCreateAPIView):
    """
    View for listing and creating FAQs.
    Allows users to view and submit frequently asked questions.
    """

    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieve the list of FAQs for the current user.
        """
        return self.queryset.filter(is_active=True)

    def perform_create(self, serializer):
        """
        Save a new FAQ and log the action.
        """
        faq = serializer.save()
        logger.info("FAQ created: %s", faq.question)


class FAQListCreateView(FAQMixin, generics.ListCreateAPIView):
    """
    API view to list and create FAQs.
    - GET: Retrieve a list of active FAQs.
    - POST: Create a new FAQ entry.

    The list shows only active FAQs (`is_active=True`).
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the FAQ list and create view.
        Calls the parent constructor.
        """
        super().__init__(*args, **kwargs)


class FAQDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, or deleting a specific FAQ.
    """

    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [IsAuthenticated]


class CourseListCreateView(CourseMixin, generics.ListCreateAPIView):
    """
    API view to list and create courses.
    - GET: Retrieve a list of active courses.
    - POST: Create a new course (teachers only).

    Only active courses are listed.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the course list and create view.
        Calls the parent constructor.
        """
        super().__init__(*args, **kwargs)


class CourseDetailView(CourseMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific course.
    - GET: Retrieve a specific course.
    - PUT: Update the course (teachers only).
    - DELETE: Delete the course (teachers only).
    """

    queryset = Course.objects.all()

    def perform_update(self, serializer):
        """
        Log the course update action.
        """
        course = serializer.save()
        logger.info("Course updated: %s", course.title)


class CourseEditView(CoursePermissionMixin, generics.UpdateAPIView):
    """
    API view to edit an existing course.
    Allows teachers to edit courses they created.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


class CourseDeleteView(CoursePermissionMixin, generics.DestroyAPIView):
    """
    API view to delete a course.
    Allows teachers to delete courses they created.
    """

    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        """
        Handle the delete action and log the deletion.
        """
        course_name = instance.title
        super().perform_destroy(instance)
        logger.info("Course deleted: %s", course_name)


class GroupCreateView(GroupMixin, generics.CreateAPIView):
    """
    API view to create a new group.
    Only authenticated users can create groups.
    """

    def perform_create(self, serializer):
        """
        Save a new group and log the action.
        """
        group = serializer.save()
        logger.info("Group created: %s", group.name)


class GroupListView(GroupMixin, generics.ListAPIView):
    """
    API view to list all groups.
    Only retrieves active groups associated with the current user.
    """

    def get_queryset(self):
        """
        Retrieve the list of active groups for the current user.
        """
        user = self.request.user
        return self.queryset.filter(teacher=user)


class GroupEditView(GroupPermissionMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific group.
    Allows users to manage groups they created.
    """

    def perform_update(self, serializer):
        """
        Save the updated group and log the action.
        """
        group = serializer.save()
        logger.info("Group updated: %s", group.name)

    def perform_destroy(self, instance):
        """
        Delete the group and log the action.
        """
        logger.info("Group deleted: %s", instance.name)
        super().perform_destroy(instance)


class GroupDetailView(GroupPermissionMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting a specific group.
    Only the teacher who created the group can modify it.
    """

    def perform_update(self, serializer):
        """
        Save the updated group and log the action.
        """
        group = serializer.save()
        logger.info("Group updated: %s", group.name)


class LessonListView(generics.ListAPIView):
    """
    View for listing lessons.
    Allows users to view lessons.
    """

    queryset = Lesson.active.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieve the list of active lessons for the current user.
        """
        return self.queryset.filter(is_active=True)


class LessonCreateView(LessonActionMixin, generics.CreateAPIView):
    """
    View for creating lessons.
    Allows users to submit lessons.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class LessonEditView(
    LessonPermissionMixin, LessonActionMixin, generics.RetrieveUpdateDestroyAPIView
):
    """
    View for retrieving, updating, or deleting a specific lesson.
    Allows teachers to manage lessons they created.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class LessonDetailView(LessonPermissionMixin, generics.RetrieveAPIView):
    """
    View for retrieving a specific lesson.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class HomeworkListCreateView(HomeworkActionMixin, generics.ListCreateAPIView):
    """
    View for listing and creating homework assignments.
    Allows users to view and submit homework assignments.
    """

    queryset = Homework.active.all()
    serializer_class = HomeworkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieve the list of homework assignments for the current user.
        """
        return self.queryset.filter(submitted_by=self.request.user)

    def list(self, request, *args, **kwargs):
        """
        Override the list method to return only the homeworks for the current user.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class HomeworkDetailView(HomeworkActionMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, or deleting a specific homework assignment.
    Also allows teachers to grade homework submissions.
    """

    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        homework = self.get_object()

        if request.user.user_type == "teacher":
            grade_serializer = HomeworkGradeSerializer(homework, data=request.data)
            if grade_serializer.is_valid():
                grade_serializer.save()
                logger.info(
                    "Homework graded: %s with grade %d",
                    homework.title,
                    grade_serializer.validated_data["grade"],
                )
                return Response(grade_serializer.data, status=status.HTTP_200_OK)
            return Response(grade_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)


class HomeworkSubmissionView(HomeworkActionMixin, generics.CreateAPIView):
    """
    View for submitting homework.
    Allows users to submit their homework assignments.
    """

    queryset = Homework.active.all()
    serializer_class = HomeworkSubmissionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        homework_id = self.request.data.get("homework_id")
        if homework_id:
            serializer.context["homework_id"] = homework_id
            submission = serializer.save()
            logger.info("Homework submitted: %s", submission.title)


class LessonCalendarView(generics.ListAPIView):
    """
    View for displaying lessons in a calendar format.
    Allows users to see their lessons scheduled by date.
    """

    serializer_class = LessonCalendarSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieve the list of lessons for the current user within a specific date range.
        """
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")
        return Lesson.objects.filter(
            date__range=[start_date, end_date], user=self.request.user
        ).order_by("date")


class ReminderView(generics.ListAPIView):
    """
    View for listing homework reminders based on user type.

    If the user is a teacher, it returns homeworks that need to be reviewed.
    If the user is a student, it returns homeworks that are due for submission.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = HomeworkSerializer

    def get_queryset(self):
        """
        Retrieve the list of homework objects based on the user's role.

        Returns:
            QuerySet: A queryset of homework objects that are either
            pending review for teachers or due for submission for students.
        """
        user = self.request.user
        now = timezone.now()

        if user.is_teacher:
            return Homework.objects.filter(
                lesson__course__groups__teacher=user,
                review_deadline__lte=now,
                submitted_by__isnull=False,
            )
        else:
            return Homework.objects.filter(
                lesson__course__groups__students=user,
                due_date__lte=now,
            )

    def list(self, request, *args, **kwargs):
        """
        Custom list method to return reminders based on the user type.

        If the user is a teacher, it provides reminders for homework
        that needs to be reviewed. If the user is a student, it provides
        reminders for homework that needs to be submitted.

        Args:
            request: The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A Response object containing the reminder data
            and appropriate message based on the user type.
        """
        queryset = self.get_queryset()
        if request.user.is_teacher:
            return Response(
                {
                    "type": "teacher",
                    "message": "You have homeworks to review",
                    "data": self.get_serializer(queryset, many=True).data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "type": "student",
                    "message": "You have homeworks to submit",
                    "data": self.get_serializer(queryset, many=True).data,
                },
                status=status.HTTP_200_OK,
            )
