import logging
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
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
    FacebookLoginSerializer,
    GoogleLoginSerializer,
)

logger = logging.getLogger("api")
User = get_user_model()


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
                return Response({"detail": "Logout successful"})

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
            return Response(
                {
                    "message": "Email has been successfully changed. Please confirm it via the link sent to the new address."
                },
                status=status.HTTP_200_OK,
            )

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
                    return Response(
                        {"message": "Password has been reset successfully."},
                        status=status.HTTP_200_OK,
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


class GoogleLoginView(generics.GenericAPIView):
    """
    API View for Google login.
    """

    serializer_class = GoogleLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle Google login.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        return Response({"message": "Login successful", "user": user.id})


class FacebookLoginView(generics.GenericAPIView):
    """
    API View for Facebook login.
    """

    serializer_class = FacebookLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle Facebook login.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        return Response({"message": "Login successful", "user": user.id})
