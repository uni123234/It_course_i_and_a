import logging
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from rest_framework.response import Response
from calendar import monthrange
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q, Count, Case, When
from ..models import (
    Course,
    Homework,
    Lesson,
    Group,
    GroupMembership,
    HomeworkSubmission,
)
from ..serializers import (
    CourseSerializer,
    GroupCreateUpdateSerializer,
    TeacherCourseSerializer,
    LessonSerializer,
    HomeworkSerializer,
    HomeworkSubmissionSerializer,
    HomeworkGradeSerializer,
    LessonCalendarSerializer,
    MembershipRoleSerializer,
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
            Q(teacher=user) | Q(groups__memberships__user=user)
        ).distinct()

    def get_serializer_class(self):
        """
        Determine the serializer class to use based on the user role.
        If the user is a teacher, use the TeacherCourseSerializer;
        otherwise, use the default CourseSerializer.

        Returns:
            Serializer: The appropriate serializer class for the current user.
        """
        if Group.objects.filter(teacher=self.request.user).exists():
            return TeacherCourseSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        """
        Handle the creation of a new course.
        Assigns the authenticated user as the teacher for the newly created course,
        creates a group for the course, and assigns the specified lessons to the course.

        Args:
            serializer (Serializer): The serializer instance used to validate and save the course data.

        Returns:
            Response: A response containing the created course details.
        """
        user = self.request.user
        course = serializer.save(teacher=user)

        lessons = self.request.data.get("lessons")
        if lessons:
            course.lessons.set(lessons)

        group = Group.objects.create(course=course)
        group.memberships.create(user=user, role="teacher")
        course.groups.add(group)

        logger.info("Course and group created by %s: %s", user.email, course.title)
        return Response(
            {"id": course.id, "title": course.title, "description": course.description},
            status=status.HTTP_201_CREATED,
        )

    def list(self, request, *args, **kwargs):
        """
        Handle GET requests to list all courses with additional data for pie chart and user roles.
        """
        queryset = self.get_queryset()
        user = request.user

        courses_data = []
        for course in queryset:
            serializer = self.get_serializer(course)
            is_teacher = course.teacher == user
            is_student = course.groups.filter(memberships__user=user).exists()

            role = "teacher" if is_teacher else "student" if is_student else "none"

            pie_chart_data = course.groups.annotate(
                num_students=Count(Case(When(memberships__role="student", then=1))),
                num_teachers=Count(Case(When(memberships__role="teacher", then=1))),
                num_assistants=Count(Case(When(memberships__role="assistant", then=1))),
            ).values("num_students", "num_teachers", "num_assistants")

            course_data = {
                "course": serializer.data,
                "role": role,
                "pie_chart_data": pie_chart_data,
            }
            courses_data.append(course_data)

        return Response(courses_data, status=status.HTTP_200_OK)


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, or deleting a course.
    Allows access based on user roles (teacher or student in the groups).

    Attributes:
        serializer_class (CourseSerializer): Serializer for Course objects.
        permission_classes (list): List of permission classes applied to the view.
    """

    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieve the queryset of courses accessible by the authenticated user.
        Returns courses where the user is the teacher or a student in the groups associated with the courses.

        Returns:
            QuerySet: A queryset of Course objects accessible by the authenticated user.
        """
        user = self.request.user
        return Course.objects.filter(
            Q(teacher=user) | Q(groups__memberships__user=user)
        ).distinct()

    def get_object(self):
        """
        Retrieve the specific course instance if accessible by the authenticated user.
        Raises a permission error if the user is not enrolled in the course.

        Returns:
            Course: The course instance accessible by the authenticated user.
        """
        course = super().get_object()
        user = self.request.user

        if (
            user != course.teacher
            and not course.groups.filter(memberships__user=user).exists()
        ):
            raise PermissionDenied("You are not enrolled in this course.")

        return course

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve the course details along with user role information.

        Args:
            request (HttpRequest): The HTTP request.

        Returns:
            Response: A response containing the course details and user role information.
        """
        course = self.get_object()
        user = self.request.user

        is_teacher = user == course.teacher
        is_student = course.groups.filter(memberships__user=user).exists()

        serializer = self.get_serializer(course)
        return Response(
            {
                "course": serializer.data,
                "is_teacher": is_teacher,
                "is_student": is_student,
            }
        )


class CourseEditView(generics.UpdateAPIView):
    """
    View for updating a course. Allows teachers to edit the course details.

    Attributes:
        serializer_class (CourseSerializer): Serializer for Course objects.
        permission_classes (list): List of permission classes applied to the view.
    """

    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieve the queryset of courses for editing, specific to the authenticated user.
        Ensures the user is the teacher of the course.

        Returns:
            QuerySet: A queryset of Course objects for editing.
        """
        user = self.request.user
        course_id = self.kwargs.get("pk")

        queryset = Course.objects.filter(id=course_id, teacher=user)

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
        group = serializer.save()
        group.memberships.create(user=self.request.user, role="teacher")
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
        student_groups = Group.objects.filter(
            memberships__user=user, memberships__role="student"
        ).values_list("id", flat=True)

        student_lessons = Lesson.objects.filter(course__groups__id__in=student_groups)
        teacher_lessons = Lesson.objects.filter(course__teacher=user)

        return student_lessons | teacher_lessons

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        lessons_with_roles = []
        for lesson in queryset:
            lesson_data = self.get_serializer(lesson).data
            if lesson.course.teacher == request.user:
                lesson_data["user_role"] = "teacher"
            else:
                lesson_data["user_role"] = "student"
            lessons_with_roles.append(lesson_data)

        return Response(lessons_with_roles)


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


class TeacherHomeworkDetailView(generics.RetrieveAPIView):
    """
    View for retrieving homework details from the teacher's perspective.
    Provides information on the students in the course, their submission statuses, and grades.
    """

    permission_classes = [IsAuthenticated, IsCourseTeacher]
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a homework assignment by ID with student submission details.
        """
        instance = self.get_object()
        course = instance.course
        students = GroupMembership.objects.filter(
            group__course=course, role="student"
        ).select_related("user")

        student_submissions = []
        for membership in students:
            user = membership.user
            submission = HomeworkSubmission.objects.filter(
                homework=instance, student=user
            ).first()

            student_submissions.append(
                {
                    "student": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                    },
                    "submission_status": "submitted" if submission else "not_submitted",
                    "grade": submission.grade if submission else None,
                }
            )

        homework_data = self.get_serializer(instance).data
        homework_data["student_submissions"] = student_submissions

        return Response(homework_data)


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
        """
        Retrieve the list of homework assignments for the authenticated user.
        If 'course_id' is provided as a query parameter, filter by course.
        """
        course_id = self.request.query_params.get("course_id")
        user = self.request.user

        logger.info(f"User: {user}, Course ID: {course_id}")

        if course_id is None:
            logger.warning("No course_id provided in request.")
            return Homework.objects.none()

        queryset = Homework.objects.filter(
            lesson__course_id=course_id,
            lesson__course__is_active=True,
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

    def list(self, request, *args, **kwargs):
        """
        Handle GET requests to list all homework assignments with lesson information.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class HomeworkDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, or deleting a specific homework assignment.
    """

    permission_classes = [IsAuthenticated]
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a homework assignment by ID with submission details for all students in the course.
        """
        instance = self.get_object()
        user = request.user

        if user != instance.course.teacher:
            return Response(
                {"error": "Only the course teacher can view this information."},
                status=status.HTTP_403_FORBIDDEN,
            )

        submissions = HomeworkSubmission.objects.filter(homework=instance)
        students = GroupMembership.objects.filter(
            group__course=instance.course, role="student"
        )

        submission_data = HomeworkSubmissionSerializer(submissions, many=True).data
        students_data = [
            {
                "student": student.user.email,
                "submitted": any(sub.user == student.user for sub in submissions),
                "grade": next(
                    (sub.grade for sub in submissions if sub.student == student.user),
                    None,
                ),
            }
            for student in students
        ]

        homework_data = self.get_serializer(instance).data
        homework_data["submissions"] = submission_data
        homework_data["students"] = students_data

        return Response(homework_data)


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
    queryset = HomeworkSubmission.objects.all()

    def perform_update(self, serializer):
        """
        Save the updated homework grade and log the grading.

        Args:
            serializer: The serializer instance containing the updated grade data.
        """
        homework_submission = serializer.save()
        logger.info("Homework graded: %s", homework_submission.homework.title)


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


class ChangeRoleView(generics.UpdateAPIView):
    """
    View for changing the role of a user in a group.
    Only the teacher of the group can change the roles of the members.
    """

    serializer_class = MembershipRoleSerializer
    permission_classes = [IsAuthenticated, IsCourseTeacher]

    def get_object(self):
        """
        Retrieve the membership object based on the group and user provided in the request.
        """
        group_id = self.kwargs.get("group_id")
        user_id = self.kwargs.get("user_id")
        return GroupMembership.objects.get(group_id=group_id, user_id=user_id)

    def update(self, request, *args, **kwargs):
        """
        Update the role of the user in the group.
        Only allow the course owner to change the role to 'teacher'.
        """
        membership = self.get_object()
        current_user = request.user
        course_owner = membership.group.course.teacher

        if (
            "role" in request.data
            and request.data["role"] == "teacher"
            and current_user != course_owner
        ):
            return Response(
                {"detail": "Only course owner can assign teachers."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(membership, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
