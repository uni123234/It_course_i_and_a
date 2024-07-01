from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from .models import EmailChangeRequest
import json
import secrets

User = get_user_model()


@csrf_exempt
def request_email_change(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = request.user
        new_email = data.get("new_email")

        if not new_email:
            return JsonResponse({"error": "New email is required"}, status=400)

        token = secrets.token_urlsafe(50)
        email_change_request = EmailChangeRequest.objects.create(
            user=user, new_email=new_email, token=token
        )

        # Send confirmation email with token here...

        return JsonResponse(
            {
                "message": "Email change requested. Please check your new email for confirmation link."
            }
        )
    return JsonResponse({"error": "Invalid request method"}, status=400)
