from django.urls import path
from . import views

app_name = "edit2"

urlpatterns = [
    path("password-change/", views.edit_password, name="edit_password"),
]
