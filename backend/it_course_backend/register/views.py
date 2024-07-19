from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import RegistrationForm
from .models import SignInAttempt
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

@csrf_exempt
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            SignInAttempt.objects.create(user=user, timestamp=timezone.now())
            return JsonResponse({"message": "Registration successful"}, status=201)
        else:
            return JsonResponse({"errors": form.errors}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=400)
