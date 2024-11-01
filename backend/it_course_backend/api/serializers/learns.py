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


from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Course model, including homework progress.
    """
    homework_progress = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def validate_title(self, value):
        """Validate that the course title is not empty and meets length requirements."""
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        if len(value) < 5:
            raise serializers.ValidationError(
                "Title must be at least 5 characters long."
            )
        return value

    def create(self, validated_data):
        """
        Create a new Course instance and assign the teacher.
        """
        validated_data["teacher"] = self.context["request"].user
        course = Course.objects.create(**validated_data)
        return course

    def get_homework_progress(self, obj):
        """Return the homework progress for the course."""
        return obj.homework_progress()



class GroupCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating or updating a Group.
    """

    class Meta:
        model = Group
        fields = ["id", "name", "teacher", "students"]

    def create(self, validated_data):
        """Assign the requesting user as the teacher during group creation."""
        validated_data["teacher"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Update group details including teachers and students."""
        instance.name = validated_data.get("name", instance.name)
        instance.save()

        teacher = validated_data.get("teacher")
        if teacher and teacher in User.objects.all():
            instance.teacher.set(teacher)

        students = validated_data.get("students")
        if students and all(student in User.objects.all() for student in students):
            instance.students.set(students)

        return instance

    def validate_students(self, value):
        """Validate that at least one student is assigned to the group."""
        if not value:
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
        fields = [
            "title",
            "description",
        ]

    def create(self, validated_data):
        """Assign the requesting user as the teacher during course creation."""
        validated_data["teacher"] = self.context["request"].user
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
