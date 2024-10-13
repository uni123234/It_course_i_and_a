from django.contrib import admin
from .models import (
    FAQ,
)
from .models import EmailChangeRequest
from django.contrib.auth.admin import UserAdmin


# @admin.register(Course)
# class CourseAdmin(admin.ModelAdmin):
#     list_display = ("id", "name", "teacher")
#     search_fields = ("name", "teacher__username")
#     list_filter = ("teacher",)
#     ordering = ("id",)
#     fieldsets = ((None, {"fields": ("name", "description", "teacher")}),)


# @admin.register(Enrollment)
# class EnrollmentAdmin(admin.ModelAdmin):
#     list_display = ("id", "course", "student", "enrolled_at")
#     search_fields = ("course__name", "student__username")
#     list_filter = ("course", "student")
#     ordering = ("-enrolled_at",)
#     fieldsets = ((None, {"fields": ("course", "student", "enrolled_at")}),)
#     readonly_fields = ("enrolled_at",)


# @admin.register(EmailChangeRequest)
# class EmailChangeRequestAdmin(admin.ModelAdmin):
#     list_display = ("user", "new_email", "token", "created_at")
#     list_filter = ("created_at",)
#     search_fields = ("user__username", "new_email")


# class PasswordChangeRequestAdmin(admin.ModelAdmin):
#     list_display = ("user", "new_password", "token", "created_at")
#     search_fields = ("user__username", "token")
#     list_filter = ("user", "created_at")
#     ordering = ("-created_at",)
#     readonly_fields = ("created_at",)

#     fieldsets = (
#         (None, {"fields": ("user", "new_password", "token")}),
#         (
#             "Timestamps",
#             {
#                 "fields": ("created_at",),
#             },
#         ),
#     )

#     def get_readonly_fields(self, request, obj=None):
#         if obj:
#             return self.readonly_fields + ("user", "new_password", "token")
#         return self.readonly_fields


# admin.site.register(PasswordChangeRequest, PasswordChangeRequestAdmin)


# class GroupChatAdmin(admin.ModelAdmin):
#     list_display = ("course", "user", "message", "sent_at")
#     search_fields = ("course__name", "user__username", "message")
#     list_filter = ("course", "user", "sent_at")
#     ordering = ("-sent_at",)
#     readonly_fields = ("sent_at",)

#     fieldsets = (
#         (None, {"fields": ("course", "user", "message")}),
#         (
#             "Timestamps",
#             {
#                 "fields": ("sent_at",),
#             },
#         ),
#     )

#     def get_readonly_fields(self, request, obj=None):
#         if obj:
#             return self.readonly_fields + ("course", "user", "message")
#         return self.readonly_fields


# admin.site.register(GroupChat, GroupChatAdmin)

# admin.site.register(HelpRequest)
# admin.site.register(ITCourse)
# admin.site.register(LoginAttempt)
# admin.site.register(RegisterAttempt)
# admin.site.register(EmailResetRequest)
# admin.site.register(PasswordReset)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question",)
