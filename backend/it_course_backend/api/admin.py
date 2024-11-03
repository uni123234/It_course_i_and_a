from django.contrib import admin
from .models import (
    Course,
    Group,
    Homework,
    Lesson,
    User,
)
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _


class UserAdmin(BaseUserAdmin):
    """Define admin model for custom User model."""

    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_active",
        "user_type",
        "date_joined",
        "date_updated",
    )
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("is_active", "user_type", "date_joined")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "user_type")}),
        (
            _("Permissions"),
            {"fields": ("is_active", "is_staff", "is_superuser", "user_permissions")},
        ),
        (
            _("Important dates"),
            {"fields": ("last_login", "date_joined", "date_updated")},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "user_type",
                ),
            },
        ),
    )

    def get_queryset(self, request):
        """Override get_queryset to return the user list."""
        return super().get_queryset(request).select_related("groups")

    def save_model(self, request, obj, form, change):
        """Override save_model to handle password encryption."""
        if not change:
            obj.set_password(form.cleaned_data["password1"])
        else:
            if form.cleaned_data["password1"]:
                obj.set_password(form.cleaned_data["password1"])
        super().save_model(request, obj, form, change)


class LessonAdmin(admin.ModelAdmin):
    """Admin interface for the Lesson model."""

    list_display = ("title", "course", "scheduled_time", "is_active")
    search_fields = ("title", "course__title")
    list_filter = ("course", "scheduled_time", "is_active")


class HomeworkAdmin(admin.ModelAdmin):
    """Admin interface for the Homework model."""

    list_display = (
        "title",
        "due_date",
        "submitted_by",
        "submission_date",
        "is_active",
        "is_late",
    )
    search_fields = ("title", "submitted_by__email")
    list_filter = (
        "submitted_by",
        "is_active",
        "due_date",
    )

    def is_late(self, obj):
        """Return whether the homework is submitted late."""
        return obj.is_late

    is_late.boolean = True
    is_late.short_description = "Late Submission"


class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "teacher")
    search_fields = ("title", "teacher__email")
    list_filter = ("teacher",)



class GroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "teacher")
    search_fields = ("name", "teacher__email")
    list_filter = ("teacher",)


admin.site.register(Group, GroupAdmin)
admin.site.register(Homework, HomeworkAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(User, UserAdmin)
