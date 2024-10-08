"""
URL configuration for the API.

This module contains URL patterns for API endpoints.
"""

from django.urls import path
from .views import (
    CourseListView,
    GoogleLoginView,
    GroupListView,
    # GroupChatListCreateView,
    HomeView,
    HomeworkListCreateView,
    LMSView,
    LessonListCreateView,
    LessonListView,
    LoginView,
    LogoutView,
    RegisterView,
    PasswordResetConfirmView,
    EmailChangeRequestView,
    EditPasswordView,
    # RequestHelpView,
)

app_name = "api"

urlpatterns = [
    path("course/", CourseListView.as_view(), name="course_list"),
    path("edit_email/", EmailChangeRequestView.as_view(), name="request_email_change"),
    path("edit_password/", EditPasswordView.as_view(), name="edit_password"),
    # path("group_chat/", GroupChatListCreateView.as_view(), name="group_chat"),
    # path("help/", RequestHelpView.as_view(), name="request_help"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "reset_password/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="reset_password",
    ),
    path("google-login/", GoogleLoginView.as_view(), name="google_login"),
    path("", HomeView.as_view(), name="home"),
    path("lms/", LMSView.as_view(), name="lms"),
    path('lessons/', LessonListView.as_view(), name='lesson_list'),
    path('groups/', GroupListView.as_view(), name='group_list'),
    path(
        "course/<int:course_id>/lessons/",
        LessonListCreateView.as_view(),
        name="lesson_list_create",
    ),
    path(
        "lesson/<int:lesson_id>/homeworks/",
        HomeworkListCreateView.as_view(),
        name="homework_list_create",
    ),
]
