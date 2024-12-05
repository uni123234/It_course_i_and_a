from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils import timezone
from django.core.validators import EmailValidator
from django.utils.crypto import get_random_string
from django.conf import settings


class CustomUserManager(BaseUserManager):
    """
    Custom manager for User model with no username field.
    Users are identified by their email addresses.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required")
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
    """
    Custom user model where email is the unique identifier.
    """

    email = models.EmailField(unique=True, validators=[EmailValidator()])
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email

    def update_last_login(self):
        """Update the last login time for the user."""
        self.last_login = timezone.now()
        self.save(update_fields=["last_login"])

    def deactivate(self):
        """Deactivate the user account."""
        self.is_active = False
        self.save(update_fields=["is_active"])

    def activate(self):
        """Activate the user account."""
        self.is_active = True
        self.save(update_fields=["is_active"])


class ActiveManager(models.Manager):
    """
    Manager to retrieve only active objects.
    """

    def get_queryset(self):
        """Returns only active objects."""
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
        """Mark the object as inactive."""
        self.is_active = False
        self.save(update_fields=["is_active"])

    def activate(self):
        """Mark the object as active."""
        self.is_active = True
        self.save(update_fields=["is_active"])


class Course(ActiveModel):
    """Model representing a course, including details such as title, description, associated teacher, and course state."""

    COURSE_STATE_CHOICES = (
        ("not_started", "Not Started"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    )
    groups = models.ManyToManyField("Group", related_name="courses")
    enrollment_code = models.CharField(
        max_length=10, unique=True, default=get_random_string(10)
    )
    lessons = models.ManyToManyField("Lesson", related_name="courses_in_lesson")
    start_date = models.DateField(default=timezone.now)
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

    def homework_progress(self):
        """
        Calculate and return the homework submission progress for each lesson in the course.

        Returns:
            List[Dict]: A list of dictionaries containing homework progress data for each lesson.
        """
        progress_data = []
        for lesson in self.lessons.all():
            total_homework = lesson.homework_set.count()
            submitted_homework = lesson.homework_set.filter(
                submitted_by__isnull=False
            ).count()

            progress_percentage = (
                (submitted_homework / total_homework * 100) if total_homework > 0 else 0
            )

            progress_data.append(
                {
                    "lesson_title": lesson.title,
                    "total_homework": total_homework,
                    "submitted_homework": submitted_homework,
                    "progress_percentage": progress_percentage,
                }
            )

        return progress_data

    def save(self, *args, **kwargs):
        if not self.enrollment_code:
            self.enrollment_code = get_random_string(10)
        super().save(*args, **kwargs)


class Lesson(ActiveModel):
    """
    Model representing a lesson, including its title, content,
    scheduled time, and related course.
    """

    title = models.CharField(max_length=255, verbose_name="Title")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
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

    def get_user_role(self, user):
        """
        Determine the role of the user (teacher or student) for this lesson.
        """
        if self.course.teacher == user:
            return "teacher"
        elif self.course.groups.filter(
            memberships__user=user, memberships__role="student"
        ).exists():
            return "student"
        return "none"


class Homework(ActiveModel):
    """
    Model representing a homework assignment.
    """

    title = models.CharField(max_length=255)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
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
        return f"Homework for {self.lesson.title if hasattr(self, 'lesson') else 'No Lesson'}"

    @property
    def is_late(self):
        """
        Check if the homework is submitted late.
        """
        return (
            (self.submission_date > self.due_date)
            if self.submission_date and self.due_date
            else False
        )

    class Meta:
        ordering = ["due_date"]


class HomeworkSubmission(ActiveModel):
    """
    Model representing a student's submission for a homework assignment.
    """

    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    submission_text = models.TextField()
    submission_file = models.FileField(
        upload_to="homework_submissions/", blank=True, null=True
    )
    submission_image = models.ImageField(
        upload_to="homework_images/", blank=True, null=True
    )
    submission_date = models.DateTimeField(auto_now_add=True)
    grade = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"Submission by {self.student} for {self.homework.title}"


class GroupMembership(ActiveModel):
    """
    Intermediate model representing the membership of a user in a group.
    """

    ROLE_CHOICES = (
        ("student", "Student"),
        ("teacher", "Teacher"),
        ("assistant", "Assistant"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey("Group", on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="student")

    class Meta:
        unique_together = ("user", "group")

    def __str__(self):
        return f"{self.user} - {self.group} ({self.role})"


class Group(ActiveModel):
    """
    Model representing a student group.
    """

    name = models.CharField(max_length=255)
    course = models.ForeignKey(
        "Course",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="student_groups",
    )
    memberships = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through=GroupMembership
    )

    def __str__(self):
        return self.name

    @property
    def student_count(self):
        """Return the number of students in the group."""
        return self.memberships.filter(groupmembership__role="student").count()

    @property
    def has_teacher(self):
        """Check if the group has an assigned teacher."""
        return self.memberships.filter(groupmembership__role="teacher").exists()

    @property
    def is_completed(self):
        """Check if the group has completed its training."""
        return not self.is_active
