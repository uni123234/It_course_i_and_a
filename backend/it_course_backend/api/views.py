# from datetime import timezone
# import secrets
# import logging
# import requests
# from django.http import JsonResponse, HttpResponse
# from django.views import View
# from django.contrib.auth import get_user_model, login as auth_login
# from django.contrib.auth.tokens import default_token_generator
# from django.utils.http import urlsafe_base64_decode
# from django.utils.encoding import force_str
# from rest_framework import generics, status
# from rest_framework.permissions import (
#     IsAuthenticated,
#     AllowAny,
#     IsAuthenticatedOrReadOnly,
# )
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.exceptions import TokenError
# from .models import (
#     FAQ,
#     Course,
#     Group,
#     Homework,
#     Lesson,
#     RegisterAttempt,
#     EmailChangeRequest,
#     LoginAttempt,
# )
# from .serializers import (
#     FAQSerializer,
#     GroupSerializer,
#     HomeworkSerializer,
#     HomeworkSubmissionSerializer,
#     LessonCalendarSerializer,
#     LessonSerializer,
#     LoginSerializer,
#     RegisterSerializer,
#     CourseSerializer,
# )

# logger = logging.getLogger(__name__)
# User = get_user_model()


# class HomeView(View):
#     """
#     View to handle requests to the home page.
#     """

#     def get(self, request):
#         """
#         Handle GET requests to the home page.
#         """
#         return HttpResponse("Hello, world. You're at the home page.")


# class LMSView(View):
#     """
#     View to handle requests to the LMS endpoint.
#     """

#     def get(self, request):
#         """
#         Handle GET requests to the LMS endpoint.
#         """
#         return JsonResponse(
#             {"message": "LMS endpoint is under construction"}, status=200
#         )

#     def post(self, request):
#         """
#         Handle POST requests to the LMS endpoint.
#         """
#         return JsonResponse(
#             {"message": "LMS POST request is not yet implemented"}, status=501
#         )

# class LessonListCreateView(generics.ListCreateAPIView):
#     queryset = Lesson.objects.all()
#     serializer_class = LessonSerializer
#     permission_classes = [AllowAny]

#     def get_queryset(self):
#         course_id = self.kwargs.get("course_id")
#         return Lesson.objects.filter(course_id=course_id)


# class LessonListView(generics.ListAPIView):
#     serializer_class = LessonSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         if user.is_teacher:
#             return Lesson.objects.filter(course__groups__teacher=user)
#         else:
#             return Lesson.objects.filter(course__groups__students=user)


# class GroupListView(generics.ListAPIView):
#     serializer_class = GroupSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         if user.is_teacher:
#             return Group.objects.filter(teacher=user)
#         else:
#             return Group.objects.filter(students=user)


# class HomeworkListCreateView(generics.ListCreateAPIView):
#     queryset = Homework.objects.all()
#     serializer_class = HomeworkSerializer
#     permission_classes = [AllowAny]

#     def get_queryset(self):
#         lesson_id = self.kwargs.get("lesson_id")
#         return Homework.objects.filter(lesson_id=lesson_id)


# class CourseListView(generics.ListAPIView):
#     """
#     View to list all courses.
#     """

#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer
#     permission_classes = [AllowAny]

#     def get(self, request, *args, **kwargs):
#         """
#         Handle GET requests to list all courses.
#         """
#         response = super().get(request, *args, **kwargs)
#         logger.info("Course list retrieved successfully.")
#         return response

# class LessonCalendarView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         if user.is_teacher:
#             lessons = Lesson.objects.filter(course__teacher=user)
#         else:
#             lessons = Lesson.objects.filter(course__students=user)

#         serializer = LessonCalendarSerializer(lessons, many=True)
#         return Response(serializer.data)


# class ReminderView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         now = timezone.now()

#         if user.is_teacher:
#             homeworks_to_review = Homework.objects.filter(
#                 lesson__course__groups__teacher=user,
#                 review_deadline__lte=now,
#                 submitted_by__isnull=False,
#             )
#             serializer = HomeworkSerializer(homeworks_to_review, many=True)
#             return Response(
#                 {
#                     "type": "teacher",
#                     "message": "You have homeworks to review",
#                     "data": serializer.data,
#                 }
#             )
#         else:
#             homeworks_to_submit = Homework.objects.filter(
#                 lesson__course__groups__students=user,
#                 deadline__lte=now,
#             )
#             serializer = HomeworkSerializer(homeworks_to_submit, many=True)
#             return Response(
#                 {
#                     "type": "student",
#                     "message": "You have homeworks to submit",
#                     "data": serializer.data,
#                 }
#             )


# class HomeworkSubmissionView(APIView):
#     """
#     API View to handle homework submission.
#     """

#     def post(self, request, homework_id):
#         """
#         Handle POST request for homework submission.
#         """
#         try:
#             homework = Homework.objects.get(id=homework_id)
#             serializer = HomeworkSubmissionSerializer(data=request.data)

#             if serializer.is_valid():
#                 homework.submission_date = timezone.now()
#                 homework.submission_file = serializer.validated_data["submission_file"]
#                 homework.save()

#                 return Response(
#                     {"message": "Homework submitted successfully!"},
#                     status=status.HTTP_200_OK,
#                 )

#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Homework.DoesNotExist:
#             return Response(
#                 {"error": "Homework not found."}, status=status.HTTP_404_NOT_FOUND
#             )

#     def delete(self, request, homework_id):
#         """
#         Handle DELETE request to clear homework submission.
#         """
#         try:
#             homework = Homework.objects.get(id=homework_id)
#             homework.submission_file.delete()
#             homework.submission_file = None
#             homework.submission_date = None
#             homework.save()

#             return Response(
#                 {"message": "Homework submission cleared."}, status=status.HTTP_200_OK
#             )
#         except Homework.DoesNotExist:
#             return Response(
#                 {"error": "Homework not found."}, status=status.HTTP_404_NOT_FOUND
#             )


import logging
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response

from .models import FAQ, User
from .serializers import (
    ChangeEmailSerializer,
    ChangePasswordSerializer,
    ChangeUsernameSerializer,
    FAQSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    RegisterSerializer,
    LoginSerializer,
)

logger = logging.getLogger("api")


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        logger.info("Registration request: %s", request.data)
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = serializer.save()
        logger.info("User registered: %s", user.email)
        return Response({"message": "User has been registered.", "user": user.email})


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        logger.info("Login request: %s", request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(email=serializer.validated_data["email"])
            if not user.check_password(serializer.validated_data["password"]):
                logger.warning("Invalid credentials for: %s", user.email)
                return Response({"detail": "Invalid credentials"}, status=400)

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
                }
            )

        except User.DoesNotExist:
            logger.warning("User not found: %s", serializer.validated_data["email"])
            return Response({"detail": "Invalid credentials"}, status=400)


class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                logger.info("User logged out: %s", request.user.email)
                return Response({"detail": "Logout successful"}, status=200)
            return Response({"detail": "No refresh token provided"}, status=400)
        except Exception as er:
            logger.error("Error during logout: %s", str(er))
            return Response({"detail": "Logout failed"}, status=400)


class ChangePasswordView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data["new_password"])
            request.user.save()
            logger.info(
                "User %s successfully changed their password.", request.user.username
            )
            return Response({"message": "Password has been successfully changed."})

        logger.warning(
            "User %s failed to change password: %s",
            request.user.username,
            serializer.errors,
        )
        return Response({"errors": serializer.errors})


class ChangeEmailView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangeEmailSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            request.user.email = serializer.validated_data["email"]
            request.user.save()
            logger.info(
                "User %s successfully changed their email to %s.",
                request.user.username,
                serializer.validated_data["email"],
            )
            return Response({"message": "Email has been successfully changed."})

        logger.warning(
            "User %s failed to change email: %s",
            request.user.username,
            serializer.errors,
        )
        return Response({"errors": serializer.errors})


class ChangeUsernameView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangeUsernameSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            request.user.username = serializer.validated_data["username"]
            request.user.save()
            logger.info(
                "User %s successfully changed their username to %s.",
                request.user.username,
                serializer.validated_data["username"],
            )
            return Response({"message": "Username has been successfully changed."})

        logger.warning(
            "User %s failed to change username: %s",
            request.user.username,
            serializer.errors,
        )
        return Response({"errors": serializer.errors})


class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            send_mail(
                "Password Reset Request",
                f"Use the following link to reset your password: "
                f"http://localhost:8000/reset-confirm/{uid}/{token}/",
                "from@example.com",
                [email],
                fail_silently=False,
            )

            logger.info("Password reset email sent to %s", email)
            return Response({"message": "Password reset email has been sent."})

        logger.warning("Password reset request failed: %s", serializer.errors)
        return Response({"errors": serializer.errors}, status=400)


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(pk=serializer.validated_data["uid"])
            user.set_password(serializer.validated_data["new_password"])
            user.save()

            logger.info("User %s has successfully reset their password.", user.username)
            return Response({"message": "Password has been successfully reset."})

        logger.warning("Password reset confirmation failed: %s", serializer.errors)
        return Response({"errors": serializer.errors}, status=400)


class FAQListCreateView(generics.ListCreateAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [AllowAny]


class FAQDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [AllowAny]
