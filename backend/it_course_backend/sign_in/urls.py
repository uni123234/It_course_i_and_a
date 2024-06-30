from django.urls import path
from . import views

app_name = 'sign_in'

urlpatterns = [
    path("", views.sign_in)
]
