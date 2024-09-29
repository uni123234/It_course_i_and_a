import secrets
import logging
import requests

from django.http import JsonResponse, HttpResponse
from django.views import View
from django.contrib.auth import get_user_model, login as auth_login
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .models import (
    Course,
    Group,
    Homework,
    Lesson,
    RegisterAttempt,
    EmailChangeRequest,
    LoginAttempt,
)
from .serializers import (
    GroupSerializer,
    HomeworkSerializer,
    LessonSerializer,
    LoginSerializer,
    RegisterSerializer,
    CourseSerializer,
)

logger = logging.getLogger(__name__)
User = get_user_model()


class HomeView(View):
    """
    View to handle requests to the home page.
    """

    def get(self, request):
        """
        Handle GET requests to the home page.
        """
        return HttpResponse("Hello, world. You're at the home page.")


class LMSView(View):
    """
    View to handle requests to the LMS endpoint.
    """

    def get(self, request):
        """
        Handle GET requests to the LMS endpoint.
        """
        return JsonResponse(
            {"message": "LMS endpoint is under construction"}, status=200
        )

    def post(self, request):
        """
        Handle POST requests to the LMS endpoint.
        """
        return JsonResponse(
            {"message": "LMS POST request is not yet implemented"}, status=501
        )


class RegisterView(generics.CreateAPIView):
    """
    View to handle user registration.
    """

    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        """
        Save the new user and log the registration attempt.
        """
        user = serializer.save()
        RegisterAttempt.objects.create(user=user)
        logger.info("User registered successfully: %s", user.email)


class LoginView(generics.GenericAPIView):
    """
    View to handle user login and token generation.
    """

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        """
        Handle POST requests for user login, generating JWT tokens upon successful login.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        auth_login(request, user)
        LoginAttempt.objects.create(user=user)

        refresh = RefreshToken.for_user(user)
        response_data = {
            "message": "Login successful",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "username": user.username,
                "email": user.email,
            },
        }
        logger.info("User logged in: %s", user.username)
        response = Response(response_data, status=status.HTTP_200_OK)
        response.set_cookie(
            key="sessionid",
            value=request.session.session_key,
            httponly=True,
            samesite="Lax",
        )
        return response


class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        course_id = self.kwargs.get("course_id")
        return Lesson.objects.filter(course_id=course_id)


class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_teacher:
            return Lesson.objects.filter(course__groups__teacher=user)
        else:
            return Lesson.objects.filter(course__groups__students=user)


class GroupListView(generics.ListAPIView):
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_teacher:
            return Group.objects.filter(teacher=user)
        else:
            return Group.objects.filter(students=user)


class HomeworkListCreateView(generics.ListCreateAPIView):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        lesson_id = self.kwargs.get("lesson_id")
        return Homework.objects.filter(lesson_id=lesson_id)


class LogoutView(generics.GenericAPIView):
    """
    View to handle user logout by blacklisting the refresh token.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handle POST requests to log out the user by blacklisting the provided refresh token.
        """
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info("User logged out successfully: %s", request.user.username)
            return Response(
                {"message": "Logout successful"},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except KeyError:
            logger.error("Logout error: Refresh token is required")
            return Response(
                {"error": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except TokenError:
            logger.error(
                "Logout error: Invalid token for user %s", request.user.username
            )
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


class CourseListView(generics.ListAPIView):
    """
    View to list all courses.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to list all courses.
        """
        response = super().get(request, *args, **kwargs)
        logger.info("Course list retrieved successfully.")
        return response


class EmailChangeRequestView(generics.GenericAPIView):
    """
    View to handle email change requests from authenticated users.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handle POST requests to request an email change.
        """
        new_email = request.data.get("new_email")

        if not new_email:
            logger.error("Email change error: New email is required.")
            return Response(
                {"error": "New email is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(email=new_email).exists():
            logger.error("Email change error: Email already in use.")
            return Response(
                {"error": "Email already in use"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token = secrets.token_urlsafe(50)
        EmailChangeRequest.objects.create(
            user=request.user, new_email=new_email, token=token
        )
        logger.info("Email change requested for user %s", request.user.username)
        return Response(
            {
                "message": "Email change requested. Please check your new email for confirmation link."
            }
        )


class EditPasswordView(generics.GenericAPIView):
    """
    View to handle password changes for authenticated users.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handle POST requests to change the user's password.
        """
        new_password = request.data.get("new_password")

        if not new_password:
            logger.error("Password change error: New password is required.")
            return Response(
                {"error": "New password is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.user.set_password(new_password)
        request.user.save()
        logger.info("Password changed successfully for user %s", request.user.username)
        return Response(
            {"message": "Password changed successfully."},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(generics.GenericAPIView):
    """
    View to handle password reset confirmation.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle POST requests to confirm the password reset.
        """
        token = request.data.get("token")
        new_password = request.data.get("new_password")
        uidb64 = request.data.get("uidb64")

        if not token or not new_password or not uidb64:
            logger.error(
                "Password reset confirm error: Missing token, new_password or uidb64."
            )
            return Response(
                {"error": "Token, new password, and user ID are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            logger.error("Password reset confirm error: Invalid user")
            return Response(
                {"error": "Invalid user"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not default_token_generator.check_token(user, token):
            logger.error("Password reset confirm error: Invalid token")
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()
        logger.info("Password has been reset successfully for user %s", user.username)
        return Response(
            {"message": "Password has been reset successfully."},
            status=status.HTTP_200_OK,
        )


class GoogleLoginView(APIView):
    """
    View to handle Google login and token verification.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle POST requests to log in via Google OAuth2.
        """
        id_token = request.data.get("id_token")
        if not id_token:
            logger.error("Google login error: ID token is required.")
            return Response(
                {"error": "ID token is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            response = requests.get(
                f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}"
            )
            response_data = response.json()

            if "error_description" in response_data:
                logger.error(
                    "Google login error: %s", response_data["error_description"]
                )
                return Response(
                    {"error": response_data["error_description"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            email = response_data.get("email")
            user = User.objects.filter(email=email).first()

            if user:
                auth_login(request, user)
                logger.info("User logged in via Google: %s", user.username)
            else:
                user = User.objects.create(
                    username=email.split("@")[0],
                    email=email,
                )
                auth_login(request, user)
                logger.info("New user created and logged in via Google: %s", user.email)

            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": {
                        "username": user.username,
                        "email": user.email,
                    },
                },
                status=status.HTTP_200_OK,
            )

        except requests.RequestException as e:
            logger.error("Google login error: %s", str(e))
            return Response(
                {"error": "Failed to verify ID token with Google."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
