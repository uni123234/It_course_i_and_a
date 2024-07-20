from django.urls import path
from . import views
from .views import GroupChatListCreateView, LoginView, RegisterView

app_name = 'api'

urlpatterns = [
    path("course/", views.course_list, name="course_list"),
    # path("courses/enroll/<int:course_id>/", views.enroll_in_course, name="enroll_in_course"),
    path("edit_email/", views.request_email_change, name="request_email_change"),
    path("edit_password/", views.edit_password, name="edit_password"),
    path("group_chat/", GroupChatListCreateView.as_view(), name="group_chat"),
    path("help/", views.request_help, name="request_help"),
    path("", views.home, name="home"),
    path("lms/", views.lms, name="lms"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("reset_email/", views.reset_mail, name="reset_mail"),
    path("reset_password/", views.reset_password, name="reset_password"),
    
]
