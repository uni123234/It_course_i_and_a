# login_in/models.py
from django.db import models
from django.conf import settings

class LoginAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    success = models.BooleanField()
    attempted_at = models.DateTimeField(auto_now_add=True)
