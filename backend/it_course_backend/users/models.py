from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    role = models.CharField(max_length=10, choices=[('student', 'Student'), ('teacher', 'Teacher')])
    email_verified = models.BooleanField(default=False)

    def is_email_verified(self):
        return self.email_verified
