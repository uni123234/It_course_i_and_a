from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import PasswordChangeRequest
from django.contrib.auth import get_user_model

User = get_user_model()


@csrf_exempt
def edit_password(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_id = data.get("user_id")
        new_password = data.get("new_password")
        token = data.get("token")

        try:
            user = User.objects.get(id=user_id)
            password_change_request = PasswordChangeRequest.objects.create(
                user=user, new_password=new_password, token=token
            )
            password_change_request.save()
            return JsonResponse(
                {"message": "Password change request created successfully."}
            )
        except User.DoesNotExist:
            return JsonResponse({"error": "User does not exist."}, status=400)
    return JsonResponse({"error": "Invalid request method."}, status=400)
