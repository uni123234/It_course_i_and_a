"""
This module contains custom authentication backends for the IT course application.
"""

from django.contrib.auth import get_user_model
from allauth.account.auth_backends import AuthenticationBackend


class EmailBackend(AuthenticationBackend):
    """
    Custom authentication backend that authenticates users using their email and password.
    """

    def authenticate(self, request, email=None, password=None, **kwargs):
        """
        Authenticate a user based on the provided email and password.

        Args:
            request: The HTTP request object.
            email: The email of the user attempting to log in.
            password: The password of the user attempting to log in.
            kwargs: Additional arguments passed to the authentication method.

        Returns:
            The authenticated user if successful, or None if authentication fails.
        """
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=email)
        except user_model.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None
