from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    identifier = forms.CharField(max_length=150, required=True, help_text="Username or Email")
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        identifier = cleaned_data.get('identifier')
        password = cleaned_data.get('password')

        user = User.objects.filter(username=identifier).first()
        if not user:
            user = User.objects.filter(email=identifier).first()

        if user:
            self.user = authenticate(username=user.username, password=password)
            if self.user is None:
                raise forms.ValidationError("Invalid password")
        else:
            raise forms.ValidationError("Invalid username/email")

        return cleaned_data

    def get_user(self):
        return self.user


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password")


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
