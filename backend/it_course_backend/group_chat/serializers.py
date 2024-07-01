# group_chat/serializers.py
from rest_framework import serializers
from .models import GroupChat


class GroupChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupChat
        fields = ["id", "course", "user", "message", "sent_at"]
        read_only_fields = ["sent_at"]
