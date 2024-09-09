"""
Serializers for the API application.
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import (
    Course,
    Enrollment,
    Group,
    Homework,
    Lesson,
    PasswordChangeRequest,
    RegisterAttempt,
    EmailChangeRequest,
    GroupChat,
    HelpRequest,
)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """

    class Meta:
        model = User
        fields = ["username", "password", "email", "first_name", "last_name"]
        extra_kwargs = {
            "password": {"write_only": True},
            "last_name": {"required": False},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")

        user = authenticate(username=user.username, password=password)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid email or password")


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Course model.
    """

    class Meta:
        model = Course
        fields = "__all__"


class EnrollmentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Enrollment model.
    """

    class Meta:
        model = Enrollment
        fields = "__all__"


class PasswordChangeRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for the PasswordChangeRequest model.
    """

    class Meta:
        model = PasswordChangeRequest
        fields = "__all__"


class RegisterAttemptSerializer(serializers.ModelSerializer):
    """
    Serializer for the RegisterAttempt model.
    """

    class Meta:
        model = RegisterAttempt
        fields = "__all__"


class EmailChangeRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for the EmailChangeRequest model.
    """

    class Meta:
        model = EmailChangeRequest
        fields = "__all__"


class GroupChatSerializer(serializers.ModelSerializer):
    """
    Serializer for the GroupChat model.
    """

    user = UserSerializer(read_only=True)

    class Meta:
        model = GroupChat
        fields = "__all__"


class HelpRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for the HelpRequest model.
    """

    class Meta:
        model = HelpRequest
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "course", "title", "content", "video_url", "created_at"]


class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = [
            "id",
            "lesson",
            "title",
            "description",
            "due_date",
            "submitted_by",
            "submission_date",
            "submission_file",
            "grade",
        ]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name", "course", "teacher", "students"]
