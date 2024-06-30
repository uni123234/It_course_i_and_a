from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TeacherPoint(models.Model):
    teacher = models.ForeignKey(User, related_name='points_given', on_delete=models.CASCADE)
    student = models.ForeignKey(User, related_name='points_received', on_delete=models.CASCADE)
    points = models.IntegerField()

    def __str__(self):
        return f'{self.teacher.username} gives {self.points} points to {self.student.username}'
