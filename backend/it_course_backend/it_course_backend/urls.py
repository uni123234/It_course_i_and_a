"""
URL configuration for it_course_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("course/", include("course.urls", namespace="course")),
    path("edit_email/", include("edit_email.urls", namespace="edit")),
    path("edit_password/", include("edit_password.urls", namespace="edit2")),
    path("group_chat/", include("group_chat.urls", namespace="group_chat")),
    path("help/", include("help_and_help_for_course.urls", namespace="help")),
    path("", include("home.urls", namespace="home")),
    path("lms/", include("lms_for_it.urls", namespace="lms")),
    path("login_in/", include("login_in.urls", namespace="login")),
    path("reset_email/", include("reset_email.urls", namespace="reset1")),
    path("reset_password/", include("reset_password.urls", namespace="reset2")),
    path("register/", include("register.urls", namespace="register")),
    path("chat_su/", include("teacher_chat.urls", namespace="chat_su")),
    path("t_login/", include("teacher_login.urls", namespace="t_login")),
    path("points/", include("teacher_point_add_and_edit.urls", namespace="points")),
    path("register_t/", include("teacher_register.urls", namespace="t_register")),

]
