import logging
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone

from ..models import FAQ, Course, Group, Homework, Lesson
from ..serializers import (
    CourseSerializer,
    FAQSerializer,
    GroupCreateUpdateSerializer,
    LessonCalendarSerializer,
    LessonSerializer,
    HomeworkSerializer,
    HomeworkSubmissionSerializer,
    TeacherCourseSerializer,
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


class FAQListCreateView(generics.ListCreateAPIView):
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
        Only returns active FAQs.
        """
        return self.queryset.filter(is_active=True)

    def perform_create(self, serializer):
        """
        Save a new FAQ and log the action.
        """
        faq = serializer.save()
        logger.info("FAQ created: %s", faq.question)


class FAQDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, or deleting a specific FAQ.
    """

    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [IsAuthenticated]


class CourseListView(generics.ListCreateAPIView):
    """
    View for listing and creating courses.
    Allows users to view and submit courses.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieve the list of active courses for the current user.
        """
        return self.queryset.filter(is_active=True)

    def perform_create(self, serializer):
        """
        Save a new course and log the action.
        """
        if self.request.user.user_type == "teacher":
            teacher_serializer = TeacherCourseSerializer(
                data=self.request.data, context={"request": self.request}
            )
            teacher_serializer.is_valid(raise_exception=True)
            course = teacher_serializer.save()
            logger.info("Course created by teacher: %s", course.name)
        else:
            course = serializer.save()
            logger.info("Course created: %s", course.name)


class CourseCreateView(generics.CreateAPIView):
    """
    View for creating a new course.
    Allows teachers to create courses.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Save a new course and log the action.
        """
        if self.request.user.user_type == "teacher":
            teacher_serializer = TeacherCourseSerializer(
                data=self.request.data, context={"request": self.request}
            )
            teacher_serializer.is_valid(raise_exception=True)
            course = teacher_serializer.save()
            logger.info("Course created by teacher: %s", course.name)
        else:
            course = serializer.save()
            logger.info("Course created: %s", course.name)


class CourseEditView(generics.UpdateAPIView):
    """
    View for editing an existing course.
    Allows teachers to edit courses they created.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Override to check if the user is allowed to edit the course.
        """
        course = super().get_object()
        if course.teacher != self.request.user:
            raise PermissionDenied("You do not have permission to edit this course.")
        return course


class CourseDeleteView(generics.DestroyAPIView):
    """
    View for deleting a course.
    Allows teachers to delete courses they created.
    """

    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Override to check if the user is allowed to delete the course.
        """
        course = super().get_object()
        if course.teacher != self.request.user:
            raise PermissionDenied("You do not have permission to delete this course.")
        return course

    def destroy(self, request, *args, **kwargs):
        """
        Handle the delete action and log the deletion.
        """
        course = self.get_object()
        course_name = course.name
        self.perform_destroy(course)
        logger.info("Course deleted: %s", course_name)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, or deleting a specific course.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


class GroupCreateView(generics.CreateAPIView):
    """
    View for creating groups.
    Allows users to create new groups.
    """

    queryset = Group.objects.all()
    serializer_class = GroupCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Save a new group and log the action.
        """
        group = serializer.save()
        logger.info("Group created: %s", group.name)


class GroupListView(generics.ListAPIView):
    """
    View for listing all groups.
    Allows users to view groups they are associated with.
    """

    queryset = Group.objects.all()
    serializer_class = GroupCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieve the list of groups for the current user.
        """
        user = self.request.user
        return self.queryset.filter(teacher=user)


class GroupEditView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, or deleting a specific group.
    Allows users to manage groups they created.
    """

    queryset = Group.objects.all()
    serializer_class = GroupCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

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
        instance.delete()


class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, or deleting a specific group.
    """

    queryset = Group.objects.all()
    serializer_class = GroupCreateUpdateSerializer
    permission_classes = [IsAuthenticated]


class LessonListView(generics.ListCreateAPIView):
    """
    View for listing and creating lessons.
    Allows users to view and submit lessons.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieve the list of lessons for the current user.
        """
        return self.queryset.filter(is_active=True)

    def perform_create(self, serializer):
        """
        Save a new lesson and log the action.
        """
        lesson = serializer.save()
        logger.info("Lesson created: %s", lesson.title)


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, or deleting a specific lesson.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class HomeworkListCreateView(generics.ListCreateAPIView):
    """
    View for listing and creating homework assignments.
    Allows users to view and submit homework assignments.
    """

    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieve the list of homework assignments for the current user.
        """
        return self.queryset.filter(is_active=True)

    def perform_create(self, serializer):
        """
        Save a new homework assignment and log the action.
        """
        homework = serializer.save()
        logger.info("Homework created: %s", homework.title)

    def list(self, request, *args, **kwargs):
        """
        Override the list method to return only the homeworks for the current user.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class HomeworkListView(generics.ListCreateAPIView):
    """
    View for listing and creating homework assignments.
    Allows users to view and submit homework assignments.
    """

    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieve the list of homework assignments for the current user.
        """
        return self.queryset.filter(is_active=True)

    def perform_create(self, serializer):
        """
        Save a new homework assignment and log the action.
        """
        homework = serializer.save()
        logger.info("Homework created: %s", homework.title)


class HomeworkDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, or deleting a specific homework assignment.
    """

    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer
    permission_classes = [IsAuthenticated]


class HomeworkSubmissionView(generics.CreateAPIView):
    """
    View for submitting homework.
    Allows users to submit their homework assignments.
    """

    queryset = Homework.objects.all()
    serializer_class = HomeworkSubmissionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Save a new homework submission and log the action.
        """
        submission = serializer.save()
        logger.info("Homework submitted: %s", submission.homework.title)


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
