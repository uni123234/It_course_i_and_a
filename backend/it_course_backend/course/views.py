from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment


def course_list(request):
    if request.method == "GET":
        courses = Course.objects.all().values()
        return JsonResponse(list(courses), safe=False)
    return HttpResponseBadRequest(
        {"status": "error", "message": "Invalid request method"}
    )


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
