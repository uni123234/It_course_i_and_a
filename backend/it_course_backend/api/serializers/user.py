from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth import get_user_model
from ..models import Homework, Lesson

User = get_user_model()


class HomeworkSubmissionSerializer(serializers.ModelSerializer):
    """
    Serializer for homework submission.
    """

    class Meta:
        model = Homework
        fields = ["submission_file"]

    def validate_submission_file(self, value):
        if not value:
            raise serializers.ValidationError("Submission file is required.")
        return value

    def create(self, validated_data):
        homework = Homework.objects.get(id=self.context["homework_id"])
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
            due_date__gte=now,
            submission_file__isnull=True,
        )


class HomeworkGradeSerializer(serializers.ModelSerializer):
    """
    Serializer for grading a homework submission.
    """

    class Meta:
        model = Homework
        fields = ["id", "grade"]

    def validate_grade(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Grade must be between 0 and 100.")
        return value


class LessonCalendarSerializer(serializers.ModelSerializer):
    """
    Serializer for the Lesson model to be used in the lesson calendar view.
    """

    class Meta:
        model = Lesson
        fields = ["id", "title", "content", "scheduled_time", "meeting_link"]
