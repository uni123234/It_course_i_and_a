from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import EmailValidator
from django.contrib.auth import get_user_model


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if password is None:
            raise ValueError("Superusers must have a password.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
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
        self.last_login = timezone.now()
        self.save(update_fields=["last_login"])

    def deactivate(self):
        self.is_active = False
        self.save(update_fields=["is_active"])

    def activate(self):
        self.is_active = True
        self.save(update_fields=["is_active"])


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question


class Course(models.Model):
    """
    Model representing a course, including details such as title,
    description, and associated teacher.
    """

    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="courses_taught",
        verbose_name="Teacher",
    )

    def __str__(self):
        return self.title


class Lesson(models.Model):
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

    def __str__(self):
        return f"{self.title} ({self.course.title})"


class Homework(models.Model):
    lesson = models.ForeignKey(
        "Lesson", on_delete=models.CASCADE, related_name="homeworks"
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
        return f"Homework for {self.lesson.title}"

    @property
    def is_late(self):
        return (
            self.submission_date > self.due_date
            if self.submission_date and self.due_date
            else False
        )


class Group(models.Model):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="groups")
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="teacher_groups",
        limit_choices_to={"is_teacher": True},
    )
    students = models.ManyToManyField(
        User, related_name="student_groups", limit_choices_to={"is_student": True}
    )

    def __str__(self):
        return self.name
