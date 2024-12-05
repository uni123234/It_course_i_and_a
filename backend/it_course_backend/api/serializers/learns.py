"""
Serializers for the learning management system, including
FAQ, Course, Group, Lesson, and related data structures.
"""

from rest_framework import serializers
from django.utils import timezone
from ..models import Course, Group, Lesson, User, GroupMembership
from datetime import datetime


class DateFromDatetimeField(serializers.DateField):
    """
    Custom field to accept datetime input but store as a date.

    Notes for Frontend:
        - Accepts both date and datetime formats as input.
        - Converts datetime input to date format during storage.
    """

    def to_internal_value(self, data):
        if isinstance(data, str):
            try:
                return super().to_internal_value(data)
            except serializers.ValidationError:
                pass

        if isinstance(data, datetime):
            return data.date()

        raise serializers.ValidationError("Invalid date format.")


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Course model, handling detailed course data.

    Fields:
        - homework_progress: A dynamic field showing homework progress for the course.
        - groups: Related groups associated with the course.
        - lessons: Related lessons linked to the course.
        - Other standard fields from the Course model.

    Notes for Frontend:
        - `homework_progress` is read-only and provides real-time homework statistics.
        - `groups` and `lessons` are editable relationships and must reference existing entities.
    """

    homework_progress = serializers.SerializerMethodField()
    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True)
    lessons = serializers.PrimaryKeyRelatedField(
        queryset=Lesson.objects.all(), many=True
    )

    class Meta:
        model = Course
        fields = "__all__"

    def validate_title(self, value):
        """
        Validate the course title to ensure it is descriptive enough.

        Args:
            value: Title input.

        Returns:
            Validated title.

        Raises:
            serializers.ValidationError: If the title is empty or too short.
        """
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        if len(value) < 5:
            raise serializers.ValidationError(
                "Title must be at least 5 characters long."
            )
        return value

    def create(self, validated_data):
        """
        Create a new Course instance, assigning the teacher and linking groups and lessons.

        Args:
            validated_data: Validated input data.

        Returns:
            Newly created Course instance.

        Notes for Frontend:
            - `start_date` will default to today's date if not provided.
            - The teacher field is automatically set based on the authenticated user.
        """
        validated_data.setdefault("start_date", timezone.now().date())
        validated_data["teacher"] = self.context["request"].user

        groups = validated_data.pop("groups", [])
        lessons = validated_data.pop("lessons", [])

        course = super().create(validated_data)

        course.groups.set(groups)
        course.lessons.set(lessons)

        return course

    def get_homework_progress(self, obj):
        """
        Retrieve the homework progress for the course.

        Returns:
            A progress percentage calculated by the Course model.
        """
        return obj.homework_progress()


class GroupCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating or updating a Group.

    Fields:
        - id: Unique identifier for the group.
        - name: Name of the group.
        - students: List of student users associated with the group.

    Notes for Frontend:
        - The teacher is automatically assigned during group creation.
        - At least one student must be assigned to the group.
    """

    class Meta:
        model = Group
        fields = ["id", "name", "students"]

    def create(self, validated_data):
        """
        Create a new group and assign the requesting user as the teacher.

        Args:
            validated_data: Validated input data.

        Returns:
            The newly created Group instance.
        """
        group = super().create(validated_data)
        group.memberships.create(user=self.context["request"].user, role="teacher")
        return group

    def update(self, instance, validated_data):
        """
        Update group details, including the name and associated students.

        Args:
            instance: Existing Group instance.
            validated_data: Updated data.

        Returns:
            Updated Group instance.
        """
        instance.name = validated_data.get("name", instance.name)
        instance.save()

        students = validated_data.get("students")
        if students and all(student in User.objects.all() for student in students):
            instance.students.set(students)

        return instance

    def validate_students(self, value):
        """
        Ensure at least one student is assigned to the group.

        Args:
            value: List of students.

        Returns:
            Validated list of students.

        Raises:
            serializers.ValidationError: If the list is empty.
        """
        if not value:
            raise serializers.ValidationError(
                "At least one student must be assigned to the group."
            )
        return value


class TeacherCourseSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new course by a teacher.

    Fields:
        - id: Unique identifier for the course.
        - title: Title of the course.
        - description: Brief description of the course.
        - homework_progress: Read-only field for homework progress.

    Notes for Frontend:
        - The teacher is automatically assigned based on the authenticated user.
    """

    class Meta:
        model = Course
        fields = ["id", "title", "description", "homework_progress"]

    def create(self, validated_data):
        """
        Assign the authenticated user as the teacher during course creation.

        Args:
            validated_data: Validated input data.

        Returns:
            The newly created Course instance.
        """
        validated_data["teacher"] = self.context["request"].user
        return super().create(validated_data)


class LessonSerializer(serializers.ModelSerializer):
    """
    Serializer for the Lesson model, providing detailed lesson information.

    Fields:
        - id: Unique identifier for the lesson.
        - title: Title of the lesson.
        - scheduled_time: Date and time of the lesson.
        - content: Main content of the lesson.
        - video_url: Optional video resource URL.
        - meeting_link: Optional meeting link for the lesson.
        - notes_url: Optional URL to lesson notes.
        - notes_content: Additional content for the notes.
        - course: Associated course for the lesson.
        - user_role: Dynamically indicates if the user is a teacher or student.

    Notes for Frontend:
        - The `user_role` field helps determine the user's access level.
    """

    user_role = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = [
            "id",
            "title",
            "scheduled_time",
            "content",
            "video_url",
            "meeting_link",
            "notes_url",
            "notes_content",
            "course",
            "user_role",
        ]

    def get_user_role(self, obj):
        """
        Determine the role of the requesting user for the lesson.

        Returns:
            "teacher", "student", or None based on the user's role.
        """
        request = self.context.get("request", None)
        if request:
            user = request.user
            if obj.course.teacher == user:
                return "teacher"
            elif obj.course.groups.filter(
                memberships__user=user, memberships__role="student"
            ).exists():
                return "student"
        return None


class LessonCalendarSerializer(serializers.ModelSerializer):
    """
    Serializer for Lesson objects used in calendar views.

    Fields:
        - id: Unique identifier for the lesson.
        - title: Title of the lesson.
        - content: Main content or summary of the lesson.
        - scheduled_time: Scheduled date and time of the lesson.
        - meeting_link: Optional meeting link for the lesson.

    Notes for Frontend:
        - Simplified view for calendar integration.
    """

    class Meta:
        model = Lesson
        fields = ["id", "title", "content", "scheduled_time", "meeting_link"]


class MembershipRoleSerializer(serializers.ModelSerializer):
    """
    Serializer for handling roles in group memberships.

    Fields:
        - role: The role of the user in the group (e.g., "teacher", "student").

    Notes for Frontend:
        - Used to manage roles within groups.
    """

    class Meta:
        model = GroupMembership
        fields = ["role"]
