from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class SignInAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sign-in attempt by {self.user.username} on {self.timestamp}"
