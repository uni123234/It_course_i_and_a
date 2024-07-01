from django.contrib import admin
from .models import GroupChat


class GroupChatAdmin(admin.ModelAdmin):
    list_display = ("course", "user", "message", "sent_at")
    search_fields = ("course__name", "user__username", "message")
    list_filter = ("course", "user", "sent_at")
    ordering = ("-sent_at",)
    readonly_fields = ("sent_at",)

    fieldsets = (
        (None, {"fields": ("course", "user", "message")}),
        (
            "Timestamps",
            {
                "fields": ("sent_at",),
            },
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("course", "user", "message")
        return self.readonly_fields


admin.site.register(GroupChat, GroupChatAdmin)
