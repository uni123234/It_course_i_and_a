from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "user_type")


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password", "first_name", "last_name", "user_type")

    def create(self, validated_data):
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
        user = User.objects.filter(email=attrs["email"]).first()
        if user is None or not user.check_password(attrs["password"]):
            raise serializers.ValidationError("Invalid email or password.")
        attrs["user"] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing user password.
    """

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise ValidationError("Old password is incorrect.")
        return value

    def validate_new_password(self, value):
        if len(value) < 8:
            raise ValidationError("New password must be at least 8 characters long.")
        return value


class ChangeEmailSerializer(serializers.Serializer):
    """
    Serializer for changing user email.
    """

    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        user = self.context["request"].user
        if User.objects.filter(email=value).exists() and user.email != value:
            raise ValidationError("This email is already in use.")
        return value


class ChangeUsernameSerializer(serializers.Serializer):
    """
    Serializer for changing the user's username.
    """

    username = serializers.CharField(required=True)

    def validate_username(self, value):
        user = self.context["request"].user
        if User.objects.filter(username=value).exists() and user.username != value:
            raise ValidationError("This username is already in use.")
        return value


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for handling password reset requests.
    """
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("No user with this email found."))
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming the password reset.
    """
    new_password = serializers.CharField(min_length=8)
    token = serializers.CharField()
    uid = serializers.CharField()

    def validate(self, attrs):
        UserModel = get_user_model()
        try:
            uid = urlsafe_base64_decode(attrs["uid"]).decode()
            user = UserModel.objects.get(pk=uid)
        except (ValueError, UserModel.DoesNotExist):
            user = None

        if user is None or not default_token_generator.check_token(user, attrs["token"]):
            raise serializers.ValidationError(_("Invalid token or user ID."))

        return attrs
