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
    Serializer for user details.

    Fields:
        - id: Unique identifier of the user.
        - email: User's email address.
        - first_name: User's first name.
        - last_name: User's last name.

    Notes for Frontend:
        - Use this serializer for viewing basic user information.
    """

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name")


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Fields:
        - email: User's email address.
        - password: User's password (write-only).
        - first_name: User's first name.
        - last_name: User's last name.

    Notes for Frontend:
        - Ensure email uniqueness during registration.
        - Password must be provided.
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "first_name", "last_name")

    def create(self, validated_data):
        """
        Create a new user account.

        Args:
            validated_data: The validated registration data.

        Returns:
            Newly created user instance.

        Raises:
            ValidationError: If a user with the same email already exists.
        """
        if User.objects.filter(email=validated_data["email"]).exists():
            raise ValidationError("A user with this email already exists.")

        user = User(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.

    Fields:
        - email: User's email address.
        - password: User's password (write-only).

    Notes for Frontend:
        - Validate credentials and return user details on success.
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """
        Validate the email and password combination.

        Args:
            attrs: Dictionary containing email and password.

        Returns:
            Validated data with the user instance.

        Raises:
            ValidationError: If the credentials are invalid.
        """
        email = attrs.get("email")
        password = attrs.get("password")

        user = User.objects.filter(email=email).first()

        if user is None or not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password.")

        attrs["user"] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing user passwords.

    Fields:
        - old_password: User's current password.
        - new_password: New password to be set.

    Notes for Frontend:
        - Validate the old password before setting a new one.
    """

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        """
        Validate the old password.

        Args:
            value: Old password provided by the user.

        Returns:
            The old password if valid.

        Raises:
            ValidationError: If the old password is incorrect.
        """
        user = self.context["request"].user
        if not user.check_password(value):
            raise ValidationError("Old password is incorrect.")
        return value

    def validate_new_password(self, value):
        """
        Validate the new password.

        Args:
            value: New password provided by the user.

        Returns:
            The new password if it meets requirements.

        Raises:
            ValidationError: If the new password is too short.
        """
        if len(value) < 8:
            raise ValidationError("New password must be at least 8 characters long.")
        return value

    def save(self, **kwargs):
        """
        Save the new password for the user.

        Returns:
            Updated user instance.
        """
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user


class ChangeEmailSerializer(serializers.Serializer):
    """
    Serializer for changing user email addresses.

    Fields:
        - email: New email address to be set.

    Notes for Frontend:
        - A confirmation email is sent after updating the email address.
    """

    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        """
        Validate that the email is unique and not already in use.

        Args:
            value: New email address provided by the user.

        Returns:
            The email address if valid.

        Raises:
            ValidationError: If the email is already in use.
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
    Serializer for password reset requests.

    Fields:
        - email: Email address of the user requesting the reset.

    Notes for Frontend:
        - Ensure the email exists in the system before initiating a reset.
    """

    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Validate that the email exists in the system.

        Args:
            value: Email address provided by the user.

        Returns:
            The email address if valid.

        Raises:
            ValidationError: If no user is associated with the email.
        """
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("No user with this email found."))
        return value

    def send_reset_email(self):
        """
        Send a password reset email to the user.
        """
        email = self.validated_data["email"]
        user = User.objects.get(email=email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        send_password_reset_email(user, uid, token)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming a password reset.

    Fields:
        - new_password: New password to be set.
        - token: Token provided in the reset email.
        - uid: User ID encoded in base64.

    Notes for Frontend:
        - Ensure the token and UID are valid before setting the new password.
    """

    new_password = serializers.CharField(min_length=8)
    token = serializers.CharField()
    uid = serializers.CharField()

    def validate(self, attrs):
        """
        Validate the UID and token.

        Returns:
            Validated data if the token and UID are valid.

        Raises:
            ValidationError: If the token or UID is invalid.
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
    Serializer for handling Google login.

    Fields:
        - access_token: Token retrieved from Google after authentication.

    Notes for Frontend:
        - Validate the token with Google's API to retrieve user data.
    """

    access_token = serializers.CharField(required=True)

    def validate_access_token(self, value):
        """
        Validate the access token and retrieve or create the user.

        Returns:
            User instance associated with the token.

        Raises:
            ValidationError: If the token is invalid.
        """
        user_data = self.verify_google_token(value)
        user = self.get_or_create_user(user_data)
        self.validated_data["user"] = user
        return value

    def verify_google_token(self, access_token):
        """
        Verify the Google access token.

        Args:
            access_token: Token provided by Google.

        Returns:
            User data retrieved from Google's API.

        Raises:
            ValidationError: If the token is invalid.
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
        Get or create a user based on the Google user data.

        Args:
            user_data: User information retrieved from Google.

        Returns:
            User instance.
        """
        user, created = User.objects.get_or_create(
            email=user_data["email"],
            defaults={
                "first_name": user_data["name"].split()[0],
                "last_name": " ".join(user_data["name"].split()[1:]),
            },
        )
        return user
