from django.urls import path
from . import views

app_name = 'chat_su'

urlpatterns = [
    path("", views.chat_su)
]
