from rest_framework import serializers
from django.utils import timezone
from ..models import FAQ, Course, Group, Lesson


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

    class Meta:
        model = Course
        fields = "__all__"

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_teachers(self, value):
        if not value:
            raise serializers.ValidationError("At least one teacher must be assigned to the course.")
        return value


class GroupCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating or updating a Group.
    """

    class Meta:
        model = Group
        fields = ["id", "name", "teachers", "students"]

    def create(self, validated_data):
        validated_data["teachers"] = [self.context["request"].user]  # Assign the requesting user as the teacher
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        instance.teachers.set(validated_data.get("teachers", instance.teachers.all()))
        instance.students.set(validated_data.get("students", instance.students.all()))
        return instance

    def validate_students(self, value):
        if len(value) == 0:
            raise serializers.ValidationError("At least one student must be assigned to the group.")
        return value


class TeacherCourseSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new course by a teacher.
    """

    class Meta:
        model = Course
        fields = ["title", "description"]

    def create(self, validated_data):
        validated_data["teachers"] = [self.context["request"].user]  # Assign the requesting user as the teacher
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
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_scheduled_time(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("Scheduled time must be in the future.")
        return value

    def validate(self, attrs):
        if not attrs.get("notes_url") and not attrs.get("notes_content"):
            raise serializers.ValidationError("Either notes_url or notes_content must be provided.")
        return attrs


class LessonCalendarSerializer(serializers.ModelSerializer):
    """
    Serializer for the Lesson model used in the lesson calendar view.
    """

    class Meta:
        model = Lesson
        fields = ["id", "title", "content", "scheduled_time", "meeting_link"]
