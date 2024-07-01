from django.contrib import admin
from .models import PasswordChangeRequest


class PasswordChangeRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "new_password", "token", "created_at")
    search_fields = ("user__username", "token")
    list_filter = ("user", "created_at")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

    fieldsets = (
        (None, {"fields": ("user", "new_password", "token")}),
        (
            "Timestamps",
            {
                "fields": ("created_at",),
            },
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("user", "new_password", "token")
        return self.readonly_fields


admin.site.register(PasswordChangeRequest, PasswordChangeRequestAdmin)
