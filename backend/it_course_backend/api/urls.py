"""
URL configuration for the API.

This module contains URL patterns for API endpoints.
"""

from django.urls import path
from .views import (
    ChangeEmailView,
    ChangePasswordView,
    ChangeUsernameView,
    CourseListView,
    FAQDetailView,
    FAQListCreateView,
    FAQListView,
    GoogleLoginView,
    GroupListView,
    HomeView,
    HomeworkListCreateView,
    HomeworkSubmissionView,
    LMSView,
    LessonListCreateView,
    LessonListView,
    LoginView,
    LogoutView,
    RegisterView,
    PasswordResetConfirmView,
    EmailChangeRequestView,
    EditPasswordView,
    LessonCalendarView,
    ReminderView,
)

app_name = "api"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('change-email/', ChangeEmailView.as_view(), name='change-email'),
    path('change-username/', ChangeUsernameView.as_view(), name='change-username'),
    path(
        "reset_password/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="reset_password",
    ),
    path("faq/", FAQListCreateView.as_view(), name="faq-list-create"),
    path("faq/<int:pk>/", FAQDetailView.as_view(), name="faq-detail"),
    path("course/", CourseListView.as_view(), name="course_list"),
    path("", HomeView.as_view(), name="home"),
    path("lms/", LMSView.as_view(), name="lms"),
    path("lessons/", LessonListView.as_view(), name="lesson_list"),
    path("groups/", GroupListView.as_view(), name="group_list"),
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
    path("calendar/", LessonCalendarView.as_view(), name="lesson_calendar"),
    path("reminders/", ReminderView.as_view(), name="reminders"),
    path(
        "homework/<int:homework_id>/submit/",
        HomeworkSubmissionView.as_view(),
        name="submit_homework",
    ),
    # path("group_chat/", GroupChatListCreateView.as_view(), name="group_chat"),
]
