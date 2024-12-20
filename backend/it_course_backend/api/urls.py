"""
URL configuration for the API.

This module contains URL patterns for API endpoints.
"""

from django.urls import path
from .views import (
    ChangeEmailView,
    ChangePasswordView,
    ConfirmEmailView,
    CourseEditView,
    GroupCreateView,
    GroupEditView,
    HomePageView,
    HomeworkListCreateView,
    HomeworkSubmissionView,
    HomeworkDetailView,
    HomeworkEditView,
    HomeworkGradeView,
    LessonCalendarView,
    LessonCreateView,
    LoginView,
    LogoutView,
    RegisterView,
    PasswordResetConfirmView,
    ReminderView,
    CourseListCreateView,
    GoogleLoginView,
    CourseDetailView,
    LessonEditView,
    LessonListView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    ChangeRoleView,
    TeacherHomeworkDetailView,
)

APP_NAME = "api"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("auth/google/", GoogleLoginView.as_view(), name="google-login"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("change-email/", ChangeEmailView.as_view(), name="change-email"),
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
    path("groups/<int:pk>", GroupCreateView.as_view(), name="group-list"),
    path("groups/create/", GroupCreateView.as_view(), name="group-create"),
    path(
        "groups/<int:group_id>/users/<int:user_id>/change-role/",
        ChangeRoleView.as_view(),
        name="change-role",
    ),
    path("groups/<int:pk>/edit/", GroupEditView.as_view(), name="group-edit"),
    path("course/", CourseListCreateView.as_view(), name="course_list"),
    path("course/<int:pk>/", CourseDetailView.as_view(), name="course_detail"),
    path("courses/create/", CourseListCreateView.as_view(), name="course_create"),
    path("courses/edit/<int:pk>/", CourseEditView.as_view(), name="course_edit"),
    path("lessons/", LessonListView.as_view(), name="lesson-list"),
    path("lessons/create/", LessonCreateView.as_view(), name="lesson-create"),
    path("lessons/edit/<int:pk>/", LessonEditView.as_view(), name="lesson-edit"),
    path("calendar/", LessonCalendarView.as_view(), name="lesson_calendar"),
    path("homework/", HomeworkListCreateView.as_view(), name="homework-list-create"),
    path("homework/<int:pk>/", HomeworkDetailView.as_view(), name="homework-detail"),
    path("homework/<int:pk>/edit/", HomeworkEditView.as_view(), name="homework-edit"),
    path(
        "homework/<int:pk>/submit/",
        HomeworkSubmissionView.as_view(),
        name="homework-submit",
    ),
    path(
        "homework/<int:pk>/grade/", HomeworkGradeView.as_view(), name="homework-grade"
    ),
    path(
        "homework/<int:pk>/teacher/",
        TeacherHomeworkDetailView.as_view(),
        name="teacher-homework-detail",
    ),
]
