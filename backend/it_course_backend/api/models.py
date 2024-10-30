"""
This module contains the models for the IT course backend application.
It includes models for Users, Courses, Lessons, Homework, and more.
"""

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import EmailValidator


class CustomUserManager(BaseUserManager):
    """
    Custom manager for User model with no username field.
    Users are identified by their email addresses.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular user with the given email and password.
        """
        if not email:
            raise ValueError("The Email field is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if password is None:
            raise ValueError("Superusers must have a password.")
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model where email is the unique identifier.
    """

    USER_TYPE_CHOICES = (
        ("student", "Student"),
        ("teacher", "Teacher"),
    )

    email = models.EmailField(unique=True, validators=[EmailValidator()])
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "user_type"]

    def __str__(self):
        return self.email

    def update_last_login(self):
        """
        Update the last login time for the user.
        """
        self.last_login = timezone.now()
        self.save(update_fields=["last_login"])

    def deactivate(self):
        """
        Deactivate the user account.
        """
        self.is_active = False
        self.save(update_fields=["is_active"])

    def activate(self):
        """
        Activate the user account.
        """
        self.is_active = True
        self.save(update_fields=["is_active"])


class ActiveManager(models.Manager):
    """
    Manager to retrieve only active objects.
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class ActiveModel(models.Model):
    """
    Abstract model that adds an is_active field and an active manager.
    Provides common functionality for models with an active/inactive state.
    """

    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        abstract = True

    def deactivate(self):
        """
        Mark the object as inactive.
        """
        self.is_active = False
        self.save(update_fields=["is_active"])

    def activate(self):
        """
        Mark the object as active.
        """
        self.is_active = True
        self.save(update_fields=["is_active"])


class FAQ(ActiveModel):
    """
    Model representing a Frequently Asked Question (FAQ).
    """

    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question


class Course(ActiveModel):
    """
    Model representing a course, including details such as title,
    description, associated teacher, and course state.
    """

    COURSE_STATE_CHOICES = (
        ("not_started", "Not Started"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    )

    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="courses_taught",
        verbose_name="Teacher",
    )
    state = models.CharField(
        max_length=15, choices=COURSE_STATE_CHOICES, default="not_started"
    )

    def __str__(self):
        return self.title


class Lesson(ActiveModel):
    """
    Model representing a lesson, including its title, content,
    scheduled time, and related course.
    """

    title = models.CharField(max_length=255, verbose_name="Title")
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField(verbose_name="Scheduled Time")
    content = models.TextField(blank=True, null=True, verbose_name="Content")
    video_url = models.URLField(blank=True, null=True, verbose_name="Video URL")
    meeting_link = models.URLField(blank=True, null=True, verbose_name="Meeting Link")
    notes_url = models.URLField(blank=True, null=True, verbose_name="Notes URL")
    notes_content = models.TextField(
        blank=True, null=True, verbose_name="Notes Content"
    )

    def __str__(self):
        return f"{self.title} ({self.course.title if self.course else 'No Course'})"


class Homework(ActiveModel):
    """
    Model representing a homework assignment.
    """

    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="homeworks"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="homeworks"
    )
    submission_date = models.DateTimeField(blank=True, null=True)
    submission_file = models.FileField(
        upload_to="homework_submissions/", blank=True, null=True
    )
    grade = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"Homework for {self.lesson.title if self.lesson else 'No Lesson'}"

    @property
    def is_late(self):
        """
        Check if the homework is submitted late.
        """
        return (
            self.submission_date > self.due_date
            if self.submission_date and self.due_date
            else False
        )


class Group(ActiveModel):
    """
    Model representing a student group.
    """

    name = models.CharField(max_length=255)

    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="teacher_groups",
        limit_choices_to={"user_type": "teacher"},
        verbose_name="Teacher",
    )

    students = models.ManyToManyField(
        User,
        related_name="student_groups",
        limit_choices_to={"user_type": "student"},
        verbose_name="Students",
    )

    def __str__(self):
        return self.name

    @property
    def student_count(self):
        """Return the number of students in the group."""
        return self.students.count()

    @property
    def has_teacher(self):
        """Check if the group has an assigned teacher."""
        return self.teacher is not None

    @property
    def is_completed(self):
        """Check if the group has completed its training."""
        return not self.is_active
