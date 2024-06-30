from django.urls import path
from . import views

app_name = 'reset2'

urlpatterns = [
    path("", views.reset_password)
]
