from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError("Invalid email or password")
            self.user = authenticate(username=user.username, password=password)
            if self.user is None:
                raise forms.ValidationError("Invalid email or password")
        return cleaned_data

    def get_user(self):
        return self.user


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            return email
        else:
            raise forms.ValidationError("This email is not registered. Please use an existing account.")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            return username
        else:
            raise forms.ValidationError("This username is not registered. Please use an existing account.")

    def save(self, commit=True):
        return authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])