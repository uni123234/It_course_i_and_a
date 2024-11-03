"""
Serializers for the Homework application, including submission and grading.
"""

from rest_framework import serializers
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import get_user_model
from ..models import Homework

User = get_user_model()


class HomeworkSubmissionSerializer(serializers.ModelSerializer):
    """
    Serializer for handling homework submissions.
    """

    class Meta:
        model = Homework
        fields = ["submission_file"]

    def validate_submission_file(self, value):
        """
        Validates that the submission file is provided.
        """
        if not value:
            raise serializers.ValidationError("Submission file is required.")
        return value

    def create(self, validated_data):
        """
        Creates a homework submission and updates the submission date.
        """
        homework_id = self.context.get("homework_id")
        if homework_id is None:
            raise serializers.ValidationError("Homework ID must be provided.")

        try:
            homework = Homework.objects.get(id=homework_id)
        except Homework.DoesNotExist as exc:
            raise serializers.ValidationError("Homework not found.") from exc

        homework.submission_date = timezone.now()
        homework.submission_file = validated_data["submission_file"]
        homework.save()
        return homework


class HomeworkSerializer(serializers.ModelSerializer):
    """
    Serializer for the Homework model.
    """

    class Meta:
        model = Homework
        fields = [
            "id",
            "title",
            "description",
            "due_date",
            "submitted_by",
            "submission_date",
            "submission_file",
            "grade",
            "lesson",
            "course",
        ]
        read_only_fields = ["submitted_by", "submission_date", "grade"]

    @staticmethod
    def get_homeworks(user, now):
        """
        Retrieves homework assignments for the user based on their role.

        Args:
            user: The user requesting the homework list.
            now: The current datetime for filtering due dates.

        Returns:
            Queryset of Homework objects for the user's role.
        """
        if user.user_type == "teacher":
            return Homework.objects.filter(
                submission_date__isnull=False,
                due_date__lte=now,
                submitted_by__isnull=False,
                lesson__course__groups__teacher=user,
            ).distinct()

        elif user.user_type == "student":
            return Homework.objects.filter(
                lesson__course__groups__students=user,
                due_date__gte=now,
                submitted_by=user,
            ).distinct()

        return Homework.objects.none()


class HomeworkGradeSerializer(serializers.ModelSerializer):
    """
    Serializer for grading a homework submission.
    """

    class Meta:
        model = Homework
        fields = ["id", "grade"]

    def validate_grade(self, value):
        """
        Validates that the grade is between 0 and 100.
        """
        if value < 0 or value > 100:
            raise serializers.ValidationError("Grade must be between 0 and 100.")
        return value
