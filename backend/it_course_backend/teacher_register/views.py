from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import TeacherRegistrationForm


@csrf_exempt
def register_teacher(request):
    if request.method == "POST":
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse(
                {"message": "Teacher registration successful"}, status=201
            )
        else:
            return JsonResponse({"errors": form.errors}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=400)
