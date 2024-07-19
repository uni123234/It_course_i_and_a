from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login as auth_login
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
import json
import secrets
import logging

from .models import Course, Enrollment, PasswordChangeRequest, RegisterAttempt, EmailChangeRequest, GroupChat, HelpRequest, LoginAttempt
from .serializers import GroupChatSerializer, LoginSerializer, RegisterSerializer, UserSerializer, CourseSerializer, EnrollmentSerializer, PasswordChangeRequestSerializer, RegisterAttemptSerializer, EmailChangeRequestSerializer, HelpRequestSerializer
from .forms import LoginForm, RegistrationForm


def home(request):
    return HttpResponse("Hello, world. You're at the home page.")


def lms():
    pass


def reset_mail():
    pass


def reset_password():
    pass

logger = logging.getLogger(__name__)

User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error('Registration error: %s', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def course_list(request):
    if request.method == "GET":
        courses = Course.objects.all().values()
        return JsonResponse(list(courses), safe=False)
    return HttpResponseBadRequest({"status": "error", "message": "Invalid request method"})


# @csrf_exempt
# @login_required
# def enroll_in_course(request, course_id):
#     if request.method == "POST":
#         # Ensure the user is authenticated
#         if not request.user.is_authenticated:
#             return HttpResponseForbidden(
#                 {"status": "error", "message": "User not authenticated"}
#             )

#         # Get the course and handle the enrollment
#         course = get_object_or_404(Course, id=course_id)
#         enrollment, created = Enrollment.objects.get_or_create(
#             course=course, student=request.user
#         )

#         if created:
#             return JsonResponse(
#                 {"status": "success", "message": "Enrolled successfully"}
#             )
#         else:
#             return JsonResponse({"status": "info", "message": "Already enrolled"})

#     return HttpResponseBadRequest(
#         {"status": "error", "message": "Invalid request method"}
#     )


@csrf_exempt
def request_email_change(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = request.user
        new_email = data.get("new_email")

        if not new_email:
            return JsonResponse({"error": "New email is required"}, status=400)

        token = secrets.token_urlsafe(50)
        email_change_request = EmailChangeRequest.objects.create(user=user, new_email=new_email, token=token)
        return JsonResponse({"message": "Email change requested. Please check your new email for confirmation link."})
    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def edit_password(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_id = data.get("user_id")
        new_password = data.get("new_password")
        token = data.get("token")

        try:
            user = User.objects.get(id=user_id)
            password_change_request = PasswordChangeRequest.objects.create(user=user, new_password=new_password, token=token)
            password_change_request.save()
            return JsonResponse({"message": "Password change request created successfully."})
        except User.DoesNotExist:
            return JsonResponse({"error": "User does not exist."}, status=400)
    return JsonResponse({"error": "Invalid request method."}, status=400)

class GroupChatListCreateView(generics.ListCreateAPIView):
    queryset = GroupChat.objects.all()
    serializer_class = GroupChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course_id = self.request.query_params.get("course_id")
        if course_id:
            return GroupChat.objects.filter(course_id=course_id).order_by("sent_at")
        return GroupChat.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@csrf_exempt
def request_help(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = request.user
        course_id = data.get("course_id")
        request_text = data.get("request")

        course = Course.objects.get(id=course_id)
        help_request = HelpRequest.objects.create(user=user, course=course, request=request_text)
        return JsonResponse({"message": "Help request submitted successfully"}, status=201)
    return JsonResponse({"error": "Invalid request"}, status=400)

def home(request):
    return HttpResponse("Hello, world. You're at the home page.")

@csrf_exempt
def login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            LoginAttempt.objects.create(user=user, timestamp=timezone.now())
            return JsonResponse({"message": "Login successful"}, status=200)
        else:
            username = request.POST.get('email')
            user = User.objects.filter(username=username).first()
            if user:
                LoginAttempt.objects.create(user=user, timestamp=timezone.now())
            return JsonResponse({"errors": form.errors}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            RegisterAttempt.objects.create(user=user, timestamp=timezone.now())
            return JsonResponse({"message": "Registration successful"}, status=201)
        else:
            return JsonResponse({"errors": form.errors}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=400)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            auth_login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



