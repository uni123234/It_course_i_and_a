import logging
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response


logger = logging.getLogger("api")


class HomePageView(APIView):
    """
    View for the homepage of the API.
    Provides a welcome message and status information.
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """
        Handle GET requests to display the welcome message.
        """
        data = {
            "message": "Welcome to the API!",
            "status": "success",
            "data": {"courses": [], "lessons": []},
        }
        return Response(data)
