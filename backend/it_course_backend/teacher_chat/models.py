# teacher_chat/models.py
from django.db import models
from django.conf import settings

class TeacherChat(models.Model):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher_chats')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_chats')
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
