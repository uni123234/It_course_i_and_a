"""
Serializers for the Homework application, providing functionality for 
handling submissions, retrieving assignments, and grading submissions.
"""

from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth import get_user_model
from ..models import Homework, HomeworkSubmission, Group

User = get_user_model()


class HomeworkSubmissionSerializer(serializers.ModelSerializer):
    """
    Serializer for handling homework submissions. This provides an interface
    to handle the submission data (e.g., text, files, images) from the frontend.

    Fields:
        - id: Unique identifier for the submission.
        - homework: The associated homework assignment (linked to Homework model).
        - student: The user who submitted the homework (read-only).
        - submission_text: Optional text content for the submission.
        - submission_file: Optional file attachment for the submission.
        - submission_image: Optional image attachment for the submission.
        - submission_date: The date when the homework was submitted (read-only).
        - grade: The grade assigned to this submission (read-only).

    Notes for Frontend:
        - The `student`, `submission_date`, and `grade` fields are read-only and
          will be automatically populated by the backend.
        - The `submission_file` field is validated to ensure it is provided,
          raising an error if missing.
    """

    class Meta:
        model = HomeworkSubmission
        fields = [
            "id",
            "homework",
            "student",
            "submission_text",
            "submission_file",
            "submission_image",
            "submission_date",
            "grade",
        ]
        read_only_fields = ["student", "submission_date", "grade"]

    def validate_submission_file(self, value):
        """
        Validates that the submission file is provided.

        Args:
            value: The file provided for the submission.

        Returns:
            The validated file object.

        Raises:
            serializers.ValidationError: If the file is not provided.
        """
        if not value:
            raise serializers.ValidationError("Submission file is required.")
        return value


class HomeworkSerializer(serializers.ModelSerializer):
    """
    Serializer for the Homework model. This provides details about a homework
    assignment, including its associated lesson and course.

    Fields:
        - id: Unique identifier for the homework assignment.
        - title: Title of the homework.
        - description: Detailed description or instructions for the homework.
        - due_date: The deadline for submitting the homework.
        - submitted_by: User who submitted the homework (read-only).
        - submission_date: The date when the submission was made (read-only).
        - submission_file: Optional file attached during submission.
        - grade: The grade assigned for the homework (read-only).
        - lesson: The associated lesson for the homework (retrieved dynamically).
        - course: The course associated with the homework.

    Notes for Frontend:
        - The `submitted_by`, `submission_date`, and `grade` fields are read-only
          and populated by the backend.
        - The `lesson` field is dynamically generated and includes the lesson ID
          and title if a lesson is associated.
    """

    lesson = serializers.SerializerMethodField()

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

        Notes for Frontend:
            - Teachers: Will receive a list of homework submissions for groups
              they are teaching where a submission has been made.
            - Students: Will receive their personal list of homework assignments
              where they are part of the course group.
        """
        if Group.objects.filter(teacher=user).exists():
            return Homework.objects.filter(
                submission_date__isnull=False,
                lesson__course__groups__teacher=user,
            ).distinct()

        elif Group.objects.filter(students=user).exists():
            return Homework.objects.filter(
                lesson__course__groups__students=user,
                submitted_by=user,
            ).distinct()

        return Homework.objects.none()

    def get_lesson(self, obj):
        """
        Retrieve the associated lesson for the homework.

        Args:
            obj: The Homework object being serialized.

        Returns:
            A dictionary containing the lesson ID and title if the lesson exists,
            or None if no lesson is associated.
        """
        lesson = obj.lesson
        if lesson:
            return {
                "id": lesson.id,
                "title": lesson.title,
            }
        return None


class HomeworkGradeSerializer(serializers.ModelSerializer):
    """
    Serializer for grading homework submissions. This provides a way to
    update the grade for a specific submission.

    Fields:
        - id: Unique identifier for the submission being graded.
        - grade: The grade assigned to the submission (must be between 0 and 100).

    Notes for Frontend:
        - The `id` field is used to identify the submission to be graded.
        - The `grade` field is required and must be validated to fall within the
          range of 0 to 100.
    """

    class Meta:
        model = HomeworkSubmission
        fields = ["id", "grade"]

    def validate_grade(self, value):
        """
        Validates that the grade is within the range of 0 to 100.

        Args:
            value: The grade value provided.

        Returns:
            The validated grade value.

        Raises:
            serializers.ValidationError: If the grade is not within the valid range.
        """
        if value < 0 or value > 100:
            raise serializers.ValidationError("Grade must be between 0 and 100.")
        return value
