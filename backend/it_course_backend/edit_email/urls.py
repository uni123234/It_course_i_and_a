from django.urls import path
from . import views

app_name = "edit"

urlpatterns = [
    path(
        "email-change/", views.request_email_change, name="request_email_change"
    ),
]
