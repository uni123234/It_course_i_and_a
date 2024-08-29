from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model, login as auth_login
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_bytes, force_str

import json
import secrets
import logging

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
  # pylint: disable=unused-argument
from .models import (
    Course,
    Enrollment,
    PasswordChangeRequest,
    RegisterAttempt,
    EmailChangeRequest,
    GroupChat,
    HelpRequest,
    LoginAttempt,
)
from .serializers import (
    GroupChatSerializer,
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
    CourseSerializer,
    EnrollmentSerializer,
    PasswordChangeRequestSerializer,
    RegisterAttemptSerializer,
    EmailChangeRequestSerializer,
    HelpRequestSerializer,
)
from .forms import LoginForm, RegistrationForm

logger = logging.getLogger(__name__)
User = get_user_model()


class HomeView(View):
    """
    A simple view that returns a welcome message.
    """

    def get(self, request):
        """
        Handles GET requests and returns a welcome message.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: A response containing a welcome message.
        """
        return HttpResponse("Hello, world. You're at the home page.")


class LMSView(View):
    """
    A view for the Learning Management System (LMS) endpoint.
    """

    def get(self, request):
        """
        Handles GET requests to the LMS endpoint.

        Args:
            request: The HTTP request object.

        Returns:
            JsonResponse: A placeholder response indicating the LMS endpoint
                          is under construction.
        """
        return JsonResponse(
            {"message": "LMS endpoint is under construction"}, status=200
        )

    def post(self, request):
        """
        Handles POST requests to the LMS endpoint.

        Args:
            request: The HTTP request object.

        Returns:
            JsonResponse: A response indicating the POST request is not implemented.
        """
        return JsonResponse(
            {"message": "LMS POST request is not yet implemented"}, status=501
        )


class RegisterView(APIView):
    """
    An API view for registering a new user.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handles user registration.

        Args:
            request: The HTTP request object.

        Returns:
            Response: A response containing the registered user's data or errors.
        """
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("User registered successfully: %s", serializer.data["email"])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("Registration error: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    An API view for user login.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handles user login and returns authentication tokens.

        Args:
            request: The HTTP request object.

        Returns:
            Response: A response containing tokens and user data or errors.
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
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

            response = Response(response_data, status=status.HTTP_200_OK)
            response.set_cookie(
                key="sessionid",
                value=request.session.session_key,
                httponly=True,
                samesite="Lax",
            )
            logger.info("User logged in: %s", user.username)
            return response
        logger.error("Login error: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    An API view for logging out a user by blacklisting the refresh token.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handles user logout by blacklisting the refresh token.

        Args:
            request: The HTTP request object.

        Returns:
            Response: A response indicating success or errors.
        """
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info("User logged out successfully: %s", request.user.username)
            return Response(
                {"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT
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


@method_decorator(csrf_exempt, name="dispatch")
class CourseListView(View):
    """
    A view to handle retrieving and posting course data.
    """

    def get(self, request):
        """
        Handles GET requests to retrieve a list of courses.

        Args:
            request: The HTTP request object.

        Returns:
            JsonResponse: A response containing the list of courses.
        """
        courses = list(Course.objects.all().values())
        logger.info("Course list retrieved successfully.")
        return JsonResponse(courses, safe=False)

    def post(self, request):
        """
        Handles invalid POST requests for the course list.

        Args:
            request: The HTTP request object.

        Returns:
            JsonResponse: A response indicating an invalid request method.
        """
        logger.warning("Invalid request method for course list: POST")
        return JsonResponse(
            {"status": "error", "message": "Invalid request method"}, status=400
        )


@method_decorator(csrf_exempt, name="dispatch")
class RequestEmailChangeView(View):
    """
    A view to handle requests for changing a user's email address.
    """

    def post(self, request):
        """
        Handles POST requests to request an email change.

        Args:
            request: The HTTP request object.

        Returns:
            JsonResponse: A response indicating success or errors.
        """
        if not request.user.is_authenticated:
            return JsonResponse({"error": "User not authenticated"}, status=403)

        data = json.loads(request.body)
        new_email = data.get("new_email")

        if not new_email:
            logger.error("Email change error: New email is required.")
            return JsonResponse({"error": "New email is required"}, status=400)

        if User.objects.filter(email=new_email).exists():
            logger.error("Email change error: Email already in use.")
            return JsonResponse({"error": "Email already in use"}, status=400)

        token = secrets.token_urlsafe(50)
        EmailChangeRequest.objects.create(
            user=request.user, new_email=new_email, token=token
        )
        logger.info("Email change requested for user %s", request.user.username)
        return JsonResponse(
            {
                "message": (
                    "Email change requested. Please check your new email "
                    "for confirmation link."
                )
            }
        )

    def get(self, request):
        """
        Handles invalid GET requests for email change.

        Args:
            request: The HTTP request object.

        Returns:
            JsonResponse: A response indicating an invalid request method.
        """
        logger.warning("Invalid request method for email change request: GET")
        return JsonResponse({"error": "Invalid request method"}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class EditPasswordView(View):
    """
    A view to handle password changes for authenticated users.
    """

    def post(self, request):
        """
        Handles POST requests to change a user's password.

        Args:
            request: The HTTP request object.

        Returns:
            JsonResponse: A response indicating success or errors.
        """
        if not request.user.is_authenticated:
            return JsonResponse({"error": "User not authenticated"}, status=403)

        data = json.loads(request.body)
        new_password = data.get("new_password")

        if not new_password:
            logger.error("Password change error: New password is required.")
            return JsonResponse({"error": "New password is required"}, status=400)

        user = request.user
        user.set_password(new_password)
        user.save()
        logger.info("Password changed successfully for user %s", user.username)
        return JsonResponse({"message": "Password changed successfully."}, status=200)

    def get(self, request):
        """
        Handles invalid GET requests for password change.

        Args:
            request: The HTTP request object.

        Returns:
            JsonResponse: A response indicating an invalid request method.
        """
        logger.warning("Invalid request method for password change: GET")
        return JsonResponse({"error": "Invalid request method"}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class LoginView(View):
    """
    A view to handle user login.
    """

    def post(self, request):
        """
        Handles POST requests to log in a user.

        Args:
            request: The HTTP request object.

        Returns:
            JsonResponse: A response containing success or error messages.
        """
        form = LoginForm(request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            identifier = form.cleaned_data.get("identifier")
            if identifier:
                user = User.objects.filter(email=identifier).first()

            if user:
                LoginAttempt.objects.create(user=user)
            logger.info("User logged in successfully: %s", user.email)
            return JsonResponse({"message": "Login successful"}, status=200)

        logger.error("Login error: %s", form.errors)
        return JsonResponse({"errors": form.errors}, status=400)

    def get(self, request):
        """
        Handles invalid GET requests for login.

        Args:
            request: The HTTP request object.

        Returns:
            JsonResponse: A response indicating an invalid request method.
        """
        logger.warning("Invalid request method for login: GET")
        return JsonResponse({"error": "Invalid request method"}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class RegisterView(View):
    """
    A view to handle user registration.
    """

    def post(self, request):
        """
        Handles POST requests to register a new user.

        Args:
            request: The HTTP request object.

        Returns:
            JsonResponse: A response containing success or error messages.
        """
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            RegisterAttempt.objects.create(user=user, timestamp=timezone.now())
            logger.info("User registered successfully: %s", user.email)
            return JsonResponse({"message": "User registered successfully"}, status=201)
        logger.error("Registration error: %s", form.errors)
        return JsonResponse({"errors": form.errors}, status=400)

    def get(self, request):
        """
        Handles invalid GET requests for registration.

        Args:
            request: The HTTP request object.

        Returns:
            JsonResponse: A response indicating an invalid request method.
        """
        logger.warning("Invalid request method for registration: GET")
        return JsonResponse({"error": "Invalid request method"}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class PasswordResetRequestView(View):
    """
    A view to handle password reset requests.
    """

    def post(self, request):
        """
        Handles POST requests to initiate a password reset.

        Args:
            request: The HTTP request object.

        Returns:
            JsonResponse: A response indicating success or errors.
        """
        data = json.loads(request.body)
        email = data.get("email")

        if not email:
            logger.error("Password reset request error: Email is required.")
            return JsonResponse({"error": "Email is required"}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            logger.error(
                "Password reset request error: User does not exist with email %s",
                email,
            )
            return JsonResponse({"error": "User does not exist"}, status=400)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = request.build_absolute_uri(
            reverse("password_reset_confirm", kwargs={"uidb64": uid, "token": token})
        )

        subject = "Password Reset Requested"
        message = render_to_string(
            "password_reset_email.html",
            {
                "user": user,
                "reset_link": reset_link,
            },
        )
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

        logger.info("Password reset email sent to user %s", user.email)
        return JsonResponse({"message": "Password reset email sent."}, status=200)

    def get(self, request):
        """
        Handles invalid GET requests for password reset.

        Args:
            request: The HTTP request object.

        Returns:
            JsonResponse: A response indicating an invalid request method.
        """
        logger.warning("Invalid request method for password reset request: GET")
        return JsonResponse({"error": "Invalid request method"}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class PasswordResetConfirmView(View):
    """
    A view to handle password reset confirmations.
    """

    def post(self, request, uidb64, token):
        """
        Handles POST requests to confirm and complete a password reset.

        Args:
            request: The HTTP request object.
            uidb64: The user's ID encoded in base64.
            token: The token generated for password reset.

        Returns:
            JsonResponse: A response indicating success or errors.
        """
        data = json.loads(request.body)
        new_password = data.get("new_password")

        if not new_password:
            logger.error("Password reset confirm error: New password is required.")
            return JsonResponse({"error": "New password is required"}, status=400)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            logger.error("Password reset confirm error: Invalid user")
            return JsonResponse({"error": "Invalid user"}, status=400)

        if not default_token_generator.check_token(user, token):
            logger.error("Password reset confirm error: Invalid token")
            return JsonResponse({"error": "Invalid token"}, status=400)

        user.set_password(new_password)
        user.save()
        logger.info("Password has been reset successfully for user %s", user.username)
        return JsonResponse(
            {"message": "Password has been reset successfully."}, status=200
        )

    def get(self, request, uidb64, token):
        """
        Handles invalid GET requests for password reset confirmation.

        Args:
            request: The HTTP request object.
            uidb64: The user's ID encoded in base64.
            token: The token generated for password reset.

        Returns:
            JsonResponse: A response indicating an invalid request method.
        """
        logger.warning("Invalid request method for password reset confirm: GET")
        return JsonResponse({"error": "Invalid request method"}, status=400)
