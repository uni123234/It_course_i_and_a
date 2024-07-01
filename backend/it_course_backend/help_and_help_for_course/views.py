from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import HelpRequest
import json


@csrf_exempt
def request_help(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = request.user
        course_id = data.get("course_id")
        request_text = data.get("request")

        # Assuming Course model is imported
        course = Course.objects.get(id=course_id)

        help_request = HelpRequest.objects.create(
            user=user, course=course, request=request_text
        )
        return JsonResponse(
            {"message": "Help request submitted successfully"}, status=201
        )
    return JsonResponse({"error": "Invalid request"}, status=400)
