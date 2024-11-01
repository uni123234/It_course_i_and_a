import logging
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from ..models import FAQ, Course, Homework, Lesson, Group
from ..serializers import (
    CourseSerializer,
    FAQSerializer,
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


class FAQListCreateView(generics.ListCreateAPIView):
    """
    API view to list and create FAQs.
    - GET: Retrieve a list of active FAQs.
    - POST: Create a new FAQ entry.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = FAQSerializer
    queryset = FAQ.objects.all()

    def perform_create(self, serializer):
        faq = serializer.save()
        logger.info("FAQ created: %s", faq.question)


class FAQDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, or deleting a specific FAQ.
    """

    queryset = FAQ.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = FAQSerializer


class CourseListCreateView(generics.ListCreateAPIView):
    """
    API view to list and create courses.
    - GET: Retrieve a list of active courses.
    - POST: Create a new course and an associated group.
    """

    permission_classes = [IsAuthenticated]
    queryset = Course.objects.all()

    def get_serializer_class(self):
        return (
            TeacherCourseSerializer
            if self.request.user.user_type == "teacher"
            else CourseSerializer
        )

    def perform_create(self, serializer):
        course = serializer.save(teacher=self.request.user)
        logger.info("Course created: %s", course.title)

        group = Group.objects.create(
            name=f"{course.title} Group",
            teacher=self.request.user,
        )
        logger.info("Group created for course: %s", group.name)


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific course.
    """

    permission_classes = [IsAuthenticated, IsCourseTeacher]
    queryset = Course.objects.all()
    lookup_field = "id"

    def get_serializer_class(self):
        return (
            TeacherCourseSerializer
            if self.request.user.user_type == "teacher"
            else CourseSerializer
        )

    def perform_update(self, serializer):
        course = serializer.save()
        logger.info("Course updated: %s", course.title)


class CourseEditView(generics.UpdateAPIView):
    """
    API view to edit an existing course.
    Allows teachers to edit courses they created.
    """

    permission_classes = [IsAuthenticated, IsCourseTeacher]
    queryset = Course.objects.all()

    def get_serializer_class(self):
        return (
            TeacherCourseSerializer
            if self.request.user.user_type == "teacher"
            else CourseSerializer
        )


class GroupCreateView(generics.CreateAPIView):
    """
    API view to create a new group.
    Only authenticated users can create groups.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = GroupCreateUpdateSerializer

    def perform_create(self, serializer):
        group = serializer.save(
            teacher=self.request.user
        )  # Set the teacher to the request user
        logger.info("Group created: %s", group.name)


class GroupEditView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific group.
    Allows users to manage groups they created.
    """

    permission_classes = [IsAuthenticated, IsCourseTeacher]
    serializer_class = GroupCreateUpdateSerializer
    queryset = Group.objects.all()

    def perform_update(self, serializer):
        group = serializer.save()
        logger.info("Group updated: %s", group.name)

    def perform_destroy(self, instance):
        logger.info("Group deleted: %s", instance.name)
        super().perform_destroy(instance)


class LessonCreateView(generics.CreateAPIView):
    """
    View for creating lessons.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def perform_create(self, serializer):
        lesson = serializer.save()
        logger.info("Lesson created: %s", lesson.title)


class LessonEditView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, or deleting a specific lesson.
    """

    permission_classes = [IsAuthenticated, IsCourseTeacher]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def perform_update(self, serializer):
        lesson = serializer.save()
        logger.info("Lesson updated: %s", lesson.title)

    def perform_destroy(self, instance):
        logger.info("Lesson deleted: %s", instance.title)
        super().perform_destroy(instance)


class HomeworkListCreateView(generics.ListCreateAPIView):
    """
    View for listing and creating homework assignments.
    """

    permission_classes = [IsAuthenticated]
    queryset = Homework.objects.all()

    def get_serializer_class(self):
        return (
            HomeworkSubmissionSerializer
            if self.request.method == "POST"
            else HomeworkSerializer
        )

    def perform_create(self, serializer):
        homework = serializer.save()
        logger.info("Homework created: %s", homework.title)


class HomeworkSubmissionView(generics.CreateAPIView):
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


class HomeworkDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, or deleting a specific homework assignment.
    Allows teachers to grade homework submissions.
    """

    permission_classes = [IsAuthenticated]
    queryset = Homework.objects.all()

    def get_serializer_class(self):
        if self.request.user.user_type == "teacher" and self.request.method == "PUT":
            return HomeworkGradeSerializer
        return HomeworkSerializer

    def perform_update(self, serializer):
        if self.request.user.user_type == "teacher":
            grade_serializer = HomeworkGradeSerializer(
                self.get_object(), data=self.request.data
            )
            if grade_serializer.is_valid():
                grade_serializer.save()
                logger.info(
                    "Homework graded: %s with grade %d",
                    self.get_object().title,
                    grade_serializer.validated_data["grade"],
                )
        else:
            super().perform_update(serializer)

    def perform_destroy(self, instance):
        logger.info("Homework deleted: %s", instance.title)
        super().perform_destroy(instance)


class LessonCalendarView(generics.ListAPIView):
    """
    View for displaying lessons in a calendar format.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = LessonCalendarSerializer

    def get_queryset(self):
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")
        return Lesson.objects.filter(
            date__range=[start_date, end_date], user=self.request.user
        ).order_by("date")


class ReminderView(generics.ListAPIView):
    """
    View for listing homework reminders based on user type.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = HomeworkSerializer

    def get_queryset(self):
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
