import logging
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.exceptions import ValidationError
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import UpdateAPIView

from ..serializers import (
    ChangeEmailSerializer,
    ChangePasswordSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    RegisterSerializer,
    LoginSerializer,
)

logger = logging.getLogger("api")
User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        logger.info("Registration request: %s", request.data)
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            logger.info("User registered: %s", user.email)
            return Response(
                {"message": "User has been registered successfully."},
                status=status.HTTP_201_CREATED,
            )
        else:
            logger.warning("Registration error: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        logger.info("Login request: %s", request.data)
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        logger.info("User logged in: %s", user.email)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "user_type": user.user_type,
                },
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
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
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not request.user.check_password(
                serializer.validated_data["old_password"]
            ):
                logger.warning(
                    "User %s provided incorrect old password", request.user.email
                )
                return {"errors": {"old_password": ["Old password is incorrect."]}}

            request.user.set_password(serializer.validated_data["new_password"])
            request.user.save()

            logger.info(
                "User %s successfully changed their password.", request.user.email
            )
            return {"message": "Password has been successfully changed."}

        logger.warning(
            "User %s failed to change password: %s",
            request.user.email,
            serializer.errors,
        )
        return {"errors": serializer.errors}


class ChangeEmailView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangeEmailSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            new_email = serializer.validated_data["email"]

            if User.objects.filter(email=new_email).exists():
                logger.warning("Email %s is already in use.", new_email)
                return {"errors": {"email": ["This email is already in use."]}}

            user = request.user
            serializer.save()

            logger.info("Email confirmation link sent to %s.", new_email)
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
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token, *args, **kwargs):
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


class PasswordResetRequestView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_reset_email()
        return {"message": "Password reset link has been sent."}


class PasswordResetConfirmView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, uidb64, token, *args, **kwargs):
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
                    return {"message": "Password has been reset successfully."}

                logger.warning(
                    "Invalid token for user %s during password reset.", user.email
                )
                return {"error": "The token is invalid."}
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                logger.error("Error decoding uid during password reset.")
                return {"error": "User does not exist."}

        return {"errors": serializer.errors}


class SocialLoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user = self.verify_social_login(request.data)

        if user is None:
            return Response({"error": "Invalid social login"}, status=400)

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user_type": user.user_type,
                "email": user.email,
            }
        )

    def verify_social_login(self, data):
        return User.objects.get(email=data["email"])
