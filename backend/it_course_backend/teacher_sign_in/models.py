from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TeacherSignIn(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'TeacherSignIn for {self.user.username}'
