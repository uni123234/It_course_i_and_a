from django.urls import path
from . import views

app_name = "login_in"

urlpatterns = [
    path("login-in/", views.login_in, name="login_in"),
]
