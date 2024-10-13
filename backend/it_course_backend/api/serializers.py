# """
# Serializers for the API application.
# """

# from rest_framework import serializers
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate
# from .models import (
#     FAQ,
#     Course,
#     Enrollment,
#     Group,
#     Homework,
#     Lesson,
#     PasswordChangeRequest,
#     RegisterAttempt,
#     EmailChangeRequest,
#     GroupChat,
#     HelpRequest,
# )


# class CourseSerializer(serializers.ModelSerializer):
#     """
#     Serializer for the Course model.
#     """

#     class Meta:
#         model = Course
#         fields = "__all__"


# class EnrollmentSerializer(serializers.ModelSerializer):
#     """
#     Serializer for the Enrollment model.
#     """

#     class Meta:
#         model = Enrollment
#         fields = "__all__"


# class GroupChatSerializer(serializers.ModelSerializer):
#     """
#     Serializer for the GroupChat model.
#     """

#     user = UserSerializer(read_only=True)

#     class Meta:
#         model = GroupChat
#         fields = "__all__"


# class HelpRequestSerializer(serializers.ModelSerializer):
#     """
#     Serializer for the HelpRequest model.
#     """

#     class Meta:
#         model = HelpRequest
#         fields = "__all__"


# class LessonSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Lesson
#         fields = ["id", "course", "title", "content", "video_url", "created_at"]


# class HomeworkSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Homework
#         fields = [
#             "id",
#             "lesson",
#             "title",
#             "description",
#             "due_date",
#             "submitted_by",
#             "submission_date",
#             "submission_file",
#             "grade",
#         ]


# class GroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Group
#         fields = ["id", "name", "course", "teacher", "students"]


# class LessonCalendarSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Lesson
#         fields = ["id", "title", "description", "date", "meeting_link"]

# class HomeworkSubmissionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Homework
#         fields = ['submission_file']

#     def validate_submission_file(self, value):
#         if not value:
#             raise serializers.ValidationError("Submission file is required.")
#         return value

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError

from .models import FAQ

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "user_type")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "first_name", "last_name", "user_type")

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            user_type=validated_data["user_type"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise ValidationError("Old password is incorrect.")
        return value


class ChangeEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        user = self.context["request"].user
        if User.objects.filter(email=value).exists() and user.email != value:
            raise ValidationError("This email is already in use.")
        return value


class ChangeUsernameSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)

    def validate_username(self, value):
        user = self.context["request"].user
        if User.objects.filter(username=value).exists() and user.username != value:
            raise ValidationError("This username is already in use.")
        return value


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("No user with this email found."))
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(min_length=8)
    token = serializers.CharField()
    uid = serializers.CharField()

    def validate(self, attrs):
        UserModel = get_user_model()
        try:
            uid = int(attrs["uid"])
            user = UserModel.objects.get(pk=uid)
        except (ValueError, UserModel.DoesNotExist):
            user = None

        if user is None or not default_token_generator.check_token(
            user, attrs["token"]
        ):
            raise serializers.ValidationError(_("Invalid token or user ID."))

        return attrs


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = "__all__"
