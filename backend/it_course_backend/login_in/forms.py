from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                ("This account is inactive."),
                code='inactive',
            )
        if not user.is_email_verified():
            raise forms.ValidationError(
                ("Email is not verified."),
                code='email_not_verified',
            )
