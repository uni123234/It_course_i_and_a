from django.urls import path
from . import views

app_name = "t_login"

urlpatterns = [
    path("t-login/", views.t_login, name="t_login"),
]
