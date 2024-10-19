import logging
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from ..serializers import (
    ChangeEmailSerializer,
    ChangePasswordSerializer,
    ChangeUsernameSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    RegisterSerializer,
    LoginSerializer,
)

logger = logging.getLogger("api")
User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    View for user registration.
    Allows users to create a new account.
    """

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for user registration.
        """
        logger.info("Registration request: %s", request.data)
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        """
        Save the user after registration and log the action.
        """
        user = serializer.save()
        logger.info("User registered: %s", user.email)
        return {"message": "User has been registered.", "user": user.email}


class LoginView(generics.GenericAPIView):
    """
    View for user login.
    Authenticates a user and returns tokens.
    """

    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Handle POST requests for user login.
        """
        logger.info("Login request: %s", request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(email=serializer.validated_data["email"])
            if not user.check_password(serializer.validated_data["password"]):
                logger.warning("Invalid credentials for: %s", user.email)
                return {"detail": "Invalid credentials"}

            refresh = RefreshToken.for_user(user)
            logger.info("User logged in: %s", user.email)
            return {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "user_type": user.user_type,
                },
            }

        except User.DoesNotExist:
            logger.warning("User not found: %s", serializer.validated_data["email"])
            return {"detail": "Invalid credentials"}


class LogoutView(generics.GenericAPIView):
    """
    View for user logout.
    Revokes the refresh token and logs the action.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Handle POST requests for user logout.
        """
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                logger.info("User logged out: %s", request.user.email)
                return {"detail": "Logout successful"}
            return {"detail": "No refresh token provided"}
        except Exception as er:
            logger.error("Error during logout: %s", str(er))
            return {"detail": "Logout failed"}


class ChangePasswordView(UpdateAPIView):
    """
    View for changing the user's password.
    Requires the user to be authenticated.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        """
        Handle requests to change the user's password.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not request.user.check_password(
                serializer.validated_data["old_password"]
            ):
                logger.warning(
                    "User %s provided incorrect old password", request.user.email
                )
                return Response(
                    {"errors": {"old_password": ["Old password is incorrect."]}},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            request.user.set_password(serializer.validated_data["new_password"])
            request.user.save()

            logger.info(
                "User %s successfully changed their password.", request.user.email
            )
            return Response(
                {"message": "Password has been successfully changed."},
                status=status.HTTP_200_OK,
            )

        logger.warning(
            "User %s failed to change password: %s",
            request.user.email,
            serializer.errors,
        )
        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class ChangeEmailView(UpdateAPIView):
    """
    View for changing the user's email address.
    Requires the user to be authenticated.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ChangeEmailSerializer

    def update(self, request, *args, **kwargs):
        """
        Handle requests to change the user's email address.
        """
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            new_email = serializer.validated_data["email"]

            if User.objects.filter(email=new_email).exists():
                logger.warning("Email %s is already in use.", new_email)
                return {"errors": {"email": ["This email is already in use."]}}

            user = request.user
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            confirmation_url = f"http://localhost:8000/confirm-email/{uid}/{token}/"
            send_mail(
                "Confirm your email address",
                f"Please confirm your email address by clicking the following link: {confirmation_url}",
                "no-reply@example.com",
                [new_email],
                fail_silently=False,
            )

            logger.info("Email confirmation link sent to %s.", new_email)

            user.email = new_email
            user.is_active = False
            user.save()

            logger.info(
                "User %s successfully changed their email to %s.",
                user.username,
                new_email,
            )
            return {
                "message": "Email has been successfully changed. Please confirm it via the link sent to the new address."
            }

        logger.warning(
            "User %s failed to change email: %s",
            request.user.username,
            serializer.errors,
        )
        return {"errors": serializer.errors}


class ConfirmEmailView(generics.GenericAPIView):
    """
    View for confirming the user's email address.
    Validates the confirmation token and activates the user account.
    """

    permission_classes = [AllowAny]

    def get(self, request, uidb64, token, *args, **kwargs):
        """
        Handle GET requests for email confirmation.
        """
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            logger.info(
                "User %s has successfully confirmed their email.", user.username
            )
            return {
                "message": "Email has been successfully confirmed. You can now log in."
            }
        else:
            logger.warning("Invalid confirmation token for uid: %s", uidb64)
            return {"error": "The confirmation link is invalid or has expired."}


class ChangeUsernameView(UpdateAPIView):
    """
    View for changing the user's username.
    Requires the user to be authenticated.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ChangeUsernameSerializer

    def update(self, request, *args, **kwargs):
        """
        Handle requests to change the user's username.
        """
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            new_username = serializer.validated_data["username"]

            if User.objects.filter(username=new_username).exists():
                logger.warning(
                    "User %s tried to change username to %s, but it is already taken.",
                    request.user.username,
                    new_username,
                )
                return {"errors": {"username": ["This username is already taken."]}}

            request.user.username = new_username
            request.user.save()
            logger.info(
                "User %s successfully changed their username to %s.",
                request.user.username,
                new_username,
            )
            return {"message": "Username has been successfully changed."}

        logger.warning(
            "User %s failed to change username: %s",
            request.user.username,
            serializer.errors,
        )
        return {"errors": serializer.errors}


class PasswordResetRequestView(generics.GenericAPIView):
    """
    View for requesting a password reset.
    Sends an email with instructions to reset the password.
    """

    permission_classes = [AllowAny]
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for password reset.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            reset_url = f"http://localhost:8000/reset-password/{uid}/{token}/"
            send_mail(
                "Password Reset Requested",
                f"Please click the link to reset your password: {reset_url}",
                "no-reply@example.com",
                [email],
                fail_silently=False,
            )
            logger.info("Password reset link sent to %s", email)
            return Response({"message": "Password reset link has been sent."})
        except User.DoesNotExist:
            logger.warning("Password reset requested for non-existent email: %s", email)
            return Response(
                {
                    "message": "If the email is registered, you will receive a reset link."
                }
            )


class PasswordResetConfirmView(generics.GenericAPIView):
    """
    View for confirming the password reset.
    Validates the token and updates the user's password.
    """

    permission_classes = [AllowAny]
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, uidb64, token, *args, **kwargs):
        """
        Handle POST requests to reset the password.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                uid = urlsafe_base64_decode(uidb64).decode()
                user = User.objects.get(pk=uid)

                if default_token_generator.check_token(user, token):
                    user.set_password(serializer.validated_data["new_password"])
                    user.save()

                    logger.info(
                        "User %s successfully reset their password.", user.email
                    )
                    return Response(
                        {"message": "Password has been reset successfully."}
                    )

                logger.warning(
                    "Invalid token for user %s during password reset.", user.email
                )
                return Response(
                    {"error": "The token is invalid."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                logger.error("Error decoding uid during password reset.")
                return Response(
                    {"error": "User does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )
