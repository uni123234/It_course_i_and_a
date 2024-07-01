from django.contrib import admin
from .models import EmailChangeRequest


@admin.register(EmailChangeRequest)
class EmailChangeRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "new_email", "token", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "new_email")

