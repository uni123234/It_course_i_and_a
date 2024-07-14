# group_chat/urls.py
from django.urls import path
from .views import GroupChatListCreateView

app_name = "group_chat"

urlpatterns = [
    path("", GroupChatListCreateView.as_view(), name="group_chat"),
]
