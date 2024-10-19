"""
URL configuration for the API.

This module contains URL patterns for API endpoints.
"""

from django.urls import path
from .views import (
    ChangeEmailView,
    ChangePasswordView,
    ChangeUsernameView,
    ConfirmEmailView,
    CourseEditView,
    FAQDetailView,
    FAQListCreateView,
    GroupCreateView,
    GroupEditView,
    GroupListView,
    HomePageView,
    HomeworkListCreateView,
    HomeworkSubmissionView,
    LessonCalendarView,
    LessonListView,
    LessonCreateView,
    LessonDetailView,
    LoginView,
    LogoutView,
    RegisterView,
    PasswordResetConfirmView,
    ReminderView,
    HomeworkDetailView,
    CourseListCreateView,
)

APP_NAME = "api"

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("change-email/", ChangeEmailView.as_view(), name="change-email"),
    path("change-username/", ChangeUsernameView.as_view(), name="change-username"),
    path(
        "reset_password/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="reset_password",
    ),
    path(
        "confirm-email/<uidb64>/<token>/",
        ConfirmEmailView.as_view(),
        name="confirm-email",
    ),
    path("reminders/", ReminderView.as_view(), name="reminders"),
    path('groups/', GroupListView.as_view(), name='group-list'),
    path('groups/create/', GroupCreateView.as_view(), name='group-create'),
    path('groups/<int:pk>/edit/', GroupEditView.as_view(), name='group-edit'),
    path("course/", CourseListCreateView.as_view(), name="course_list"),
    path('courses/create/', CourseListCreateView.as_view(), name='course-create'),
    path('courses/edit/<int:pk>/', CourseEditView.as_view(), name='course-edit'),
    path('lessons/', LessonListView.as_view(), name='lesson-list'),
    path('lessons/create/', LessonCreateView.as_view(), name='lesson-create'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
    path("calendar/", LessonCalendarView.as_view(), name="lesson_calendar"),
    path('homework/', HomeworkListCreateView.as_view(), name='homework-list-create'),
    path('homework/<int:pk>/', HomeworkDetailView.as_view(), name='homework-detail'),
    path('homework/submit/', HomeworkSubmissionView.as_view(), name='homework-submit'),
    path("faq/", FAQListCreateView.as_view(), name="faq-list-create"),
    path("faq/<int:pk>/", FAQDetailView.as_view(), name="faq-detail"),
]
