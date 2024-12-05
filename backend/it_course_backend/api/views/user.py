import logging
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode

from rest_framework import generics, permissions, status
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from ..serializers import (
    ChangeEmailSerializer,
    ChangePasswordSerializer,
    GoogleLoginSerializer,
    LoginSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    RegisterSerializer,
)


logger = logging.getLogger("api")
User = get_user_model()


def set_cookie(response: HttpResponse, key: str, value: str, max_age: int):
    """
    Set a cookie with the given key, value, and max_age.

    Args:
        response (HttpResponse): The HTTP response to set the cookie on.
        key (str): The name of the cookie.
        value (str): The value of the cookie.
        max_age (int): The max age of the cookie in seconds.
    """
    response.set_cookie(
        key,
        value,
        max_age=max_age,
        secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
        httponly=True,
        samesite="Lax",
    )


def delete_cookie(response: HttpResponse, key: str):
    """
    Delete a cookie with the given key.

    Args:
        response (HttpResponse): The HTTP response to delete the cookie from.
        key (str): The name of the cookie to delete.
    """
    response.delete_cookie(key, path="/", domain=None)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view for obtaining JWT token pairs.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to obtain JWT token pairs and set them as cookies.

        Args:
            request (HttpRequest): The HTTP request.

        Returns:
            HttpResponse: The HTTP response with JWT tokens set as cookies.
        """
        response = super().post(request, *args, **kwargs)
        tokens = response.data
        access_token = tokens.get("access")
        refresh_token = tokens.get("refresh")

        set_cookie(response, "accessToken", access_token, 60 * 60)
        set_cookie(response, "refreshToken", refresh_token, 24 * 60 * 60)

        return response


class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom view for refreshing JWT access tokens.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to refresh JWT access tokens and update the cookie.

        Args:
            request (HttpRequest): The HTTP request.

        Returns:
            HttpResponse: The HTTP response with the new access token set as a cookie.
        """
        response = super().post(request, *args, **kwargs)
        new_access_token = response.data.get("access")

        set_cookie(response, "accessToken", new_access_token, 60 * 60)

        return response


class RegisterView(generics.CreateAPIView):
    """
    API View for user registration.
    """

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Handle user registration.
        """
        logger.info("Registration request: %s", request.data)
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            logger.info("User registered: %s", user.email)
            return Response(
                {"message": "User has been registered successfully."},
                status=status.HTTP_201_CREATED,
            )

        logger.warning("Registration error: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    """
    API View for user login.
    """

    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Handle user login.
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
            },
        }

        response = Response(response_data, status=status.HTTP_200_OK)
        set_cookie(response, "accessToken", str(refresh.access_token), 60 * 60)
        set_cookie(response, "refreshToken", str(refresh), 24 * 60 * 60)

        return response


class LogoutView(generics.GenericAPIView):
    """
    API View for user logout.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Handle user logout.
        """
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                logger.info("User logged out: %s", request.user.email)

                response = Response(
                    {"detail": "Logout successful"}, status=status.HTTP_200_OK
                )
                delete_cookie(response, "accessToken")
                delete_cookie(response, "refreshToken")
                return response

            return Response(
                {"detail": "No refresh token provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as er:
            logger.error("Error during logout: %s", str(er))
            return Response(
                {"detail": "Logout failed"}, status=status.HTTP_400_BAD_REQUEST
            )


class ChangePasswordView(UpdateAPIView):
    """
    API View for changing user password.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        """
        Update the user's password.
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

            response = Response(
                {"message": "Password has been successfully changed."},
                status=status.HTTP_200_OK,
            )
            delete_cookie(response, "accessToken")
            delete_cookie(response, "refreshToken")
            return response

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
    API View for changing user email.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ChangeEmailSerializer

    def update(self, request, *args, **kwargs):
        """
        Update the user's email.
        """
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            new_email = serializer.validated_data["email"]

            if User.objects.filter(email=new_email).exists():
                logger.warning("Email %s is already in use.", new_email)
                return Response(
                    {"errors": {"email": ["This email is already in use."]}},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = request.user
            serializer.save()

            logger.info("Email confirmation link sent to %s.", new_email)
            response = Response(
                {
                    "message": "Email has been successfully changed. Please confirm it via the link sent to the new address."
                },
                status=status.HTTP_200_OK,
            )
            delete_cookie(response, "accessToken")
            delete_cookie(response, "refreshToken")
            return response

        logger.warning(
            "User %s failed to change email: %s",
            request.user.username,
            serializer.errors,
        )
        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class ConfirmEmailView(generics.GenericAPIView):
    """
    API View for confirming user email.
    """

    permission_classes = [AllowAny]

    def get(self, request, uidb64, token, *args, **kwargs):
        """
        Confirm the user's email address.
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
            return Response(
                {
                    "message": "Email has been successfully confirmed. You can now log in."
                },
                status=status.HTTP_200_OK,
            )
        else:
            logger.warning("Invalid confirmation token for uid: %s", uidb64)
            return Response(
                {"error": "The confirmation link is invalid or has expired."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PasswordResetRequestView(generics.GenericAPIView):
    """
    API View for requesting a password reset.
    """

    permission_classes = [AllowAny]
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle password reset request.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_reset_email()
        return Response(
            {"message": "Password reset link has been sent."}, status=status.HTTP_200_OK
        )


class PasswordResetConfirmView(generics.GenericAPIView):
    """
    API View for confirming a password reset.
    """

    permission_classes = [AllowAny]
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, uidb64, token, *args, **kwargs):
        """
        Handle password reset confirmation.
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
                    response = Response(
                        {"message": "Password has been reset successfully."},
                        status=status.HTTP_200_OK,
                    )
                    delete_cookie(response, "accessToken")
                    delete_cookie(response, "refreshToken")
                    return response

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


class GoogleLoginView(generics.GenericAPIView):
    """
    API View for Google login.
    """

    serializer_class = GoogleLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Handle Google login.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        response = Response(
            {
                "message": "Login successful",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
            },
            status=status.HTTP_200_OK,
        )

        set_cookie(response, "accessToken", str(refresh.access_token), 60 * 60)
        set_cookie(response, "refreshToken", str(refresh), 24 * 60 * 60)

        return response
