from django.urls import path
from . import views

app_name = "teacher_sign_in"

urlpatterns = [
    path("register_t/", views.register_teacher, name="register_teacher"),
]
