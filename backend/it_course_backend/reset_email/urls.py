from django.urls import path
from . import views

app_name = 'reset1'

urlpatterns = [
    path("", views.reset_mail)
]
