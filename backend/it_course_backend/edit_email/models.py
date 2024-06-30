from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailChangeRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    new_email = models.EmailField()
    token = models.CharField(max_length=100)

    def __str__(self):
        return f'Email change request for {self.user.username}'
