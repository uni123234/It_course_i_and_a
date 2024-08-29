from django.urls import path
from . import views
from .views import (
    CourseListView,
    GroupChatListCreateView,
    HomeView,
    LMSView,
    LoginView,
    LogoutView,
    RegisterView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    RequestEmailChangeView,
    EditPasswordView,
    RequestHelpView,
)

app_name = 'api'

urlpatterns = [
    path("course/", CourseListView.as_view(), name="course_list"),
    path("edit_email/", RequestEmailChangeView.as_view(), name="request_email_change"),
    path("edit_password/", EditPasswordView.as_view(), name="edit_password"),
    path("group_chat/", GroupChatListCreateView.as_view(), name="group_chat"),
    path("help/", RequestHelpView.as_view(), name="request_help"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("reset_email/", PasswordResetRequestView.as_view(), name="reset_email"),
    path("reset_password/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="reset_password"),
    path("", HomeView.as_view(), name="home"),
    path("lms/", LMSView.as_view(), name="lms"),
]
