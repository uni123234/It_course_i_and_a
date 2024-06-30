from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class PasswordChangeRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    new_password = models.CharField(max_length=128)
    token = models.CharField(max_length=100)

    def __str__(self):
        return f'Password change request for {self.user.username}'
