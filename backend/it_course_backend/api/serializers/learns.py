"""
Serializers for the learning management system, including
FAQ, Course, Group, Lesson, and related data structures.
"""

from rest_framework import serializers
from django.utils import timezone
from ..models import FAQ, Course, Group, Lesson, User


class FAQSerializer(serializers.ModelSerializer):
    """
    Serializer for the FAQ model.
    """

    class Meta:
        model = FAQ
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Course model.
    """

    teachers = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all()
    )

    class Meta:
        model = Course
        fields = "__all__"

    def validate_title(self, value):
        """Validate that the course title is not empty."""
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_teachers(self, value):
        """Validate that at least one teacher is assigned to the course."""
        if not value:
            raise serializers.ValidationError(
                "At least one teacher must be assigned to the course."
            )
        return value

    def create(self, validated_data):
        """
        Create a new Course instance.
        """
        teachers_data = validated_data.pop("teachers", [])
        course = Course.objects.create(**validated_data)

        if teachers_data:
            course.teachers.set(teachers_data)

        return course


class GroupCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating or updating a Group.
    """

    class Meta:
        model = Group
        fields = ["id", "name", "teachers", "students"]

    def create(self, validated_data):
        """Assign the requesting user as the teacher during group creation."""
        validated_data["teachers"] = [self.context["request"].user]
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Update group details including teachers and students."""
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        instance.teachers.set(validated_data.get("teachers", instance.teachers.all()))
        instance.students.set(validated_data.get("students", instance.students.all()))
        return instance

    def validate_students(self, value):
        """Validate that at least one student is assigned to the group."""
        if len(value) == 0:
            raise serializers.ValidationError(
                "At least one student must be assigned to the group."
            )
        return value


class TeacherCourseSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new course by a teacher.
    """

    class Meta:
        model = Course
        fields = ["title", "description"]

    def create(self, validated_data):
        """Assign the requesting user as the teacher during course creation."""
        validated_data["teachers"] = [self.context["request"].user]
        return super().create(validated_data)


class LessonSerializer(serializers.ModelSerializer):
    """
    Serializer for the Lesson model.
    """

    class Meta:
        model = Lesson
        fields = [
            "id",
            "course",
            "title",
            "scheduled_time",
            "content",
            "video_url",
            "meeting_link",
            "notes_url",
            "notes_content",
        ]

    def validate_title(self, value):
        """Validate that the lesson title is not empty."""
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_scheduled_time(self, value):
        """Validate that the scheduled time is in the future."""
        if value <= timezone.now():
            raise serializers.ValidationError("Scheduled time must be in the future.")
        return value

    def validate(self, attrs):
        """Validate that either notes_url or notes_content is provided."""
        if not attrs.get("notes_url") and not attrs.get("notes_content"):
            raise serializers.ValidationError(
                "Either notes_url or notes_content must be provided."
            )
        return attrs


class LessonCalendarSerializer(serializers.ModelSerializer):
    """
    Serializer for the Lesson model used in the lesson calendar view.
    """

    class Meta:
        model = Lesson
        fields = ["id", "title", "content", "scheduled_time", "meeting_link"]
