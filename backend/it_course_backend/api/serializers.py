"""
Serializers for the API application.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError

from .models import FAQ, Course, Group, Homework, Lesson

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
        # Check if the user already exists
        if User.objects.filter(email=validated_data["email"]).exists():
            raise ValidationError("A user with this email already exists.")

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

    def validate(self, attrs):
        user = User.objects.filter(email=attrs["email"]).first()
        if user is None or not user.check_password(attrs["password"]):
            raise serializers.ValidationError("Invalid email or password.")
        attrs["user"] = user
        return attrs


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


class LessonSerializer(serializers.ModelSerializer):
    """
    Serializer for the Lesson model.
    """

    class Meta:
        model = Lesson
        fields = ["id", "course", "title", "scheduled_time"]

    def validate_title(self, value):
        """
        Validate that the title is not empty.
        """
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_scheduled_time(self, value):
        """
        Validate that the scheduled time is in the future.
        """
        if value <= timezone.now():
            raise serializers.ValidationError("Scheduled time must be in the future.")
        return value


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Course model.
    """

    class Meta:
        model = Course
        fields = "__all__"

    def validate_title(self, value):
        """
        Validate that the title is not empty.
        """
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_teacher(self, value):
        """
        Validate that the teacher is provided.
        """
        if value is None:
            raise serializers.ValidationError(
                "A teacher must be assigned to the course."
            )
        return value


class LessonCalendarSerializer(serializers.ModelSerializer):
    """
    Serializer for the Lesson model to be used in the lesson calendar view.
    """

    class Meta:
        model = Lesson
        fields = ["id", "title", "content", "date", "time", "meeting_link"]


class HomeworkSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = ["submission_file"]

    def validate_submission_file(self, value):
        if not value:
            raise serializers.ValidationError("Submission file is required.")
        return value


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

    @staticmethod
    def get_homeworks_to_review(user, now):
        return Homework.objects.filter(
            lesson__course__groups__teacher=user,
            review_deadline__lte=now,
            submitted_by__isnull=False,
        )

    @staticmethod
    def get_homeworks_to_submit(user, now):
        return Homework.objects.filter(
            lesson__course__groups__students=user,
            due_date__lte=now,
        )


class TeacherCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["title", "description"]

    def create(self, validated_data):
        validated_data["teacher"] = self.context["request"].user
        return super().create(validated_data)


class GroupCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name", "course", "teacher", "students"]

    def create(self, validated_data):
        validated_data["teacher"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.course = validated_data.get("course", instance.course)
        instance.save()
        instance.students.set(validated_data.get("students", instance.students.all()))
        return instance
