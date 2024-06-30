from django.urls import path
from . import views

app_name = 't_login'

urlpatterns = [
    path("", views.t_login)
]
