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
