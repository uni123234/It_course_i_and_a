from django.urls import path
from . import views

app_name = 'group_chat'

urlpatterns = [
    path("", views.group_chat)
]
