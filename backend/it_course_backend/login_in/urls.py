from django.urls import path
from . import views

app_name = "login_in"

urlpatterns = [
    path("", views.login_in, name="login_in"),
]
