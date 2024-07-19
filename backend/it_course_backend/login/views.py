from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as auth_login
from .forms import LoginForm
from .models import LoginAttempt
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

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
            username = request.POST.get('username')
            user = User.objects.filter(username=username).first()
            if user:
                LoginAttempt.objects.create(user=user, timestamp=timezone.now())
            return JsonResponse({"errors": form.errors}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=400)
