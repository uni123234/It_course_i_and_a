from django.urls import path
from . import views

app_name = 'course'

urlpatterns = [
    path("courses/", views.course_list, name="course_list"),
    path(
        "courses/enroll/<int:course_id>/", views.enroll_in_course, name="enroll_in_course"
    ),
]
