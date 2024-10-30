"""
Serializers for user-related functionality including registration,
login, and password management.
"""

import logging
import requests
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from ..utils import send_password_reset_email, send_email_confirmation


User = get_user_model()
logger = logging.getLogger("api")


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "user_type")


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user with validation for user types.
    """

    password = serializers.CharField(write_only=True)
    USER_TYPE_CHOICES = ["teacher", "student"]

    class Meta:
        model = User
        fields = ("email", "password", "first_name", "last_name", "user_type")

    def validate_user_type(self, value):
        """
        Validate that the user_type is either 'teacher' or 'student'.
        """
        if value not in self.USER_TYPE_CHOICES:
            raise serializers.ValidationError(
                f"User type must be one of: {', '.join(self.USER_TYPE_CHOICES)}."
            )
        return value

    def create(self, validated_data):
        """
        Create a new user instance.
        """
        if User.objects.filter(email=validated_data["email"]).exists():
            raise ValidationError("A user with this email already exists.")

        user = User(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            user_type=validated_data["user_type"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """
        Validate the user's email and password.
        """
        email = attrs.get("email")
        password = attrs.get("password")

        user = User.objects.filter(email=email).first()

        if user is None or not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password.")

        attrs["user"] = user
        return attrs


class ChangePasswordSerializer(serializers.ModelSerializer):
    """
    Serializer for changing user password.
    """

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        """
        Validate the old password.
        """
        user = self.context["request"].user
        if not user.check_password(value):
            raise ValidationError("Old password is incorrect.")
        return value

    def validate_new_password(self, value):
        """
        Validate the new password.
        """
        if len(value) < 8:
            raise ValidationError("New password must be at least 8 characters long.")
        return value


class ChangeEmailSerializer(serializers.ModelSerializer):
    """
    Serializer for changing user email.
    """

    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        """
        Validate that the new email is not already in use by another user.
        """
        user = self.context["request"].user
        if User.objects.filter(email=value).exists() and user.email != value:
            raise ValidationError("This email is already in use.")
        return value

    def save(self, **kwargs):
        """
        Update the user's email and send a confirmation email.
        """
        user = self.context["request"].user
        new_email = self.validated_data["email"]
        user.email = new_email
        user.is_active = False
        user.save()
        send_email_confirmation(user, new_email)


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for handling password reset requests.
    """

    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Validate that the email exists in the system.
        """
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("No user with this email found."))
        return value

    def send_reset_email(self):
        """
        Send the password reset email after validation.
        """
        email = self.validated_data["email"]
        user = User.objects.get(email=email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        send_password_reset_email(user, uid, token)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming the password reset.
    """

    new_password = serializers.CharField(min_length=8)
    token = serializers.CharField()
    uid = serializers.CharField()

    def validate(self, attrs):
        """
        Validate the UID and token.
        """
        user_model = get_user_model()
        try:
            uid = urlsafe_base64_decode(attrs["uid"]).decode()
            user = user_model.objects.get(pk=uid)
        except (ValueError, user_model.DoesNotExist):
            user = None

        if user is None or not default_token_generator.check_token(
            user, attrs["token"]
        ):
            raise serializers.ValidationError(_("Invalid token or user ID."))

        return attrs


class GoogleLoginSerializer(serializers.Serializer):
    """
    Serializer for Google login.
    """

    access_token = serializers.CharField(required=True)

    def validate_access_token(self, value):
        """
        Validate the access token and retrieve or create the user.
        """
        user_data = self.verify_google_token(value)
        user = self.get_or_create_user(user_data)
        self.validated_data["user"] = user
        return value

    def verify_google_token(self, access_token):
        """
        Verify the Google access token.
        """
        url = (
            f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={access_token}"
        )
        response = requests.get(url)
        if response.status_code != 200:
            logger.error("Google token verification failed: %s", response.text)
            raise ValidationError(_("Invalid Google token provided."))

        user_info = response.json()
        return {
            "id": user_info.get("sub"),
            "name": user_info.get("name"),
            "email": user_info.get("email"),
            "picture": user_info.get("picture"),
        }

    def get_or_create_user(self, user_data):
        """
        Get or create a user based on the provided user data.
        """
        user, created = User.objects.get_or_create(
            email=user_data["email"],
            defaults={
                "first_name": user_data["name"].split()[0],
                "last_name": " ".join(user_data["name"].split()[1:]),
                "user_type": "student",
            },
        )
        return user
