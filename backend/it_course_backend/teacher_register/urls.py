from django.urls import path
from . import views

app_name = "teacher_register"

urlpatterns = [
    path("", views.register_teacher, name="register_teacher"),
]
