from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import GroupChat
from .serializers import GroupChatSerializer


class GroupChatListCreateView(generics.ListCreateAPIView):
    queryset = GroupChat.objects.all()
    serializer_class = GroupChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course_id = self.request.query_params.get("course_id")
        if course_id:
            return GroupChat.objects.filter(course_id=course_id).order_by("sent_at")
        return GroupChat.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
