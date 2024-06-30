from django.urls import path
from . import views

app_name = 't_sign_in'

urlpatterns = [
    path("", views.t_sign_in)
]
