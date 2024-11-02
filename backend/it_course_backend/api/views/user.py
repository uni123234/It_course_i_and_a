import logging
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import UpdateAPIView
from ..serializers import (
    ChangeEmailSerializer,
    ChangePasswordSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    RegisterSerializer,
    LoginSerializer,
    GoogleLoginSerializer,
)

logger = logging.getLogger("api")
User = get_user_model()


def create_response(message=None, errors=None, status_code=status.HTTP_200_OK):
    """
    Utility function to create a standardized response.

    Args:
        message (str, optional): Message to include in the response.
        errors (dict, optional): Errors to include in the response.
        status_code (int): HTTP status code for the response.

    Returns:
        dict: A dictionary representing the response data.
    """
    response_data = {}
    if message:
        response_data["message"] = message
    if errors:
        response_data["errors"] = errors
    return response_data, status_code


class RegisterView(generics.CreateAPIView):
    """
    API View for user registration.
    """

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Handle user registration by validating the provided data and creating a new user.

        Returns:
            dict: Success or error message with appropriate status code.
        """
        logger.info("Registration request: %s", request.data)
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            logger.info("User registered: %s", user.email)
            return create_response(
                "User has been registered successfully.",
                status_code=status.HTTP_201_CREATED,
            )

        logger.warning("Registration error: %s", serializer.errors)
        return create_response(
            errors=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST
        )


class LoginView(generics.GenericAPIView):
    """
    API View for user login.
    """

    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Handle user login by validating credentials and returning tokens.

        Returns:
            dict: Success message with user data and tokens.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        response_data = {
            "message": "Login successful",
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

        response = Response(response_data, status=status.HTTP_200_OK)
        response.set_cookie(
            key="accessToken",
            value=str(refresh.access_token),
            httponly=True,
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            samesite="Lax",
        )
        response.set_cookie(
            key="refreshToken",
            value=str(refresh),
            httponly=True,
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            samesite="Lax",
        )

        return response


class LogoutView(generics.GenericAPIView):
    """
    API View for user logout.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Handle user logout by blacklisting the provided refresh token.

        Returns:
            dict: Success or error message.
        """
        refresh_token = request.data.get("refresh")
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                logger.info("User logged out: %s", request.user.email)
                return create_response("Logout successful")

            except Exception as er:
                logger.error("Error during logout: %s", str(er))
                return create_response(
                    errors={"detail": "Logout failed"},
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

        return create_response(
            errors={"detail": "No refresh token provided"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class ChangePasswordView(UpdateAPIView):
    """
    API View for changing user password.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        """
        Update the user's password if the old password is correct.

        Returns:
            dict: Success or error message.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not request.user.check_password(
                serializer.validated_data["old_password"]
            ):
                logger.warning(
                    "User %s provided incorrect old password", request.user.email
                )
                return create_response(
                    errors={"old_password": ["Old password is incorrect."]},
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            request.user.set_password(serializer.validated_data["new_password"])
            request.user.save()

            logger.info(
                "User %s successfully changed their password.", request.user.email
            )
            return create_response("Password has been successfully changed.")

        logger.warning(
            "User %s failed to change password: %s",
            request.user.email,
            serializer.errors,
        )
        return create_response(
            errors=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST
        )


class ChangeEmailView(UpdateAPIView):
    """
    API View for changing user email.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangeEmailSerializer

    def update(self, request, *args, **kwargs):
        """
        Update the user's email if the new email is not already in use.

        Returns:
            dict: Success or error message.
        """
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            new_email = serializer.validated_data["email"]

            if User.objects.filter(email=new_email).exists():
                logger.warning("Email %s is already in use.", new_email)
                return create_response(
                    errors={"email": ["This email is already in use."]},
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save()
            logger.info("Email confirmation link sent to %s.", new_email)
            return create_response(
                "Email has been successfully changed. Please confirm it via the link sent to the new address."
            )

        logger.warning(
            "User %s failed to change email: %s",
            request.user.username,
            serializer.errors,
        )
        return create_response(
            errors=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST
        )


class ConfirmEmailView(generics.GenericAPIView):
    """
    API View for confirming user email.
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, uidb64, token, *args, **kwargs):
        """
        Confirm the user's email address using the provided uid and token.

        Returns:
            dict: Success or error message.
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
            return create_response(
                "Email has been successfully confirmed. You can now log in."
            )

        logger.warning("Invalid confirmation token for uid: %s", uidb64)
        return create_response(
            errors={"error": "The confirmation link is invalid or has expired."},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class PasswordResetRequestView(generics.GenericAPIView):
    """
    API View for requesting a password reset.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle password reset request by sending a reset email.

        Returns:
            dict: Success message.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_reset_email()
        return create_response("Password reset link has been sent.")


class PasswordResetConfirmView(generics.GenericAPIView):
    """
    API View for confirming a password reset.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, uidb64, token, *args, **kwargs):
        """
        Handle password reset confirmation and update the user's password.

        Returns:
            dict: Success or error message.
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
                    return create_response("Password has been reset successfully.")

                logger.warning(
                    "Invalid token for user %s during password reset.", user.email
                )
                return create_response(
                    errors={"error": "The token is invalid."},
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                logger.error("Error decoding uid during password reset.")
                return create_response(
                    errors={"error": "User does not exist."},
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

        return create_response(
            errors=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST
        )


class GoogleLoginView(generics.GenericAPIView):
    """
    API View for Google login.
    """

    serializer_class = GoogleLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Handle Google login by validating the provided token and returning tokens.

        Returns:
            dict: Success message with user data and tokens.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        response_data = {
            "message": "Login successful",
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

        response = Response(response_data, status=status.HTTP_200_OK)
        response.set_cookie(
            key="accessToken",
            value=str(refresh.access_token),
            httponly=True,
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            samesite="Lax",
        )
        response.set_cookie(
            key="refreshToken",
            value=str(refresh),
            httponly=True,
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            samesite="Lax",
        )

        return response
