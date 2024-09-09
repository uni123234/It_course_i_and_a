from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="courses_taught",
    )


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=255)
    content = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.course.name})"


class Homework(models.Model):
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="homeworks"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    submitted_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="homeworks"
    )
    submission_date = models.DateTimeField(blank=True, null=True)
    submission_file = models.FileField(
        upload_to="homework_submissions/", blank=True, null=True
    )
    grade = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"Homework for {self.lesson.title}"


class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)


class EmailChangeRequest(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )  # Changed to OneToOneField
    new_email = models.EmailField(unique=True)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Email change request for {self.user.username}"


class PasswordChangeRequest(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )  # Changed to OneToOneField
    new_password = models.CharField(max_length=128)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password change request for {self.user.username}"


class GroupChat(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)


class HelpRequest(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )  # Changed to OneToOneField
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    request = models.TextField()
    status = models.CharField(max_length=10, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Help request by {self.user.username} for course {self.course.name}"


class ITCourse(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.OneToOneField(
        User, on_delete=models.CASCADE
    )  # Changed to OneToOneField

    def __str__(self):
        return self.title


class LoginAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Login attempt by {self.user.username} on {self.timestamp}"


class RegisterAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sign-in attempt by {self.user.username} on {self.timestamp}"


class EmailResetRequest(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )  # Changed to OneToOneField
    new_email = models.EmailField(unique=True)
    token = models.CharField(max_length=100)

    def __str__(self):
        return f"Email reset request for {self.user.username}"


class PasswordReset(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )  # Changed to OneToOneField
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


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
