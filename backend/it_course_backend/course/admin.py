from django.contrib import admin
from .models import Course, Enrollment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "teacher")
    search_fields = ("name", "teacher__username")
    list_filter = ("teacher",)
    ordering = ("id",)
    fieldsets = ((None, {"fields": ("name", "description", "teacher")}),)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("id", "course", "student", "enrolled_at")
    search_fields = ("course__name", "student__username")
    list_filter = ("course", "student")
    ordering = ("-enrolled_at",)
    fieldsets = ((None, {"fields": ("course", "student", "enrolled_at")}),)
    readonly_fields = ("enrolled_at",)
