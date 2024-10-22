import logging
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

logger = logging.getLogger(__name__)


def send_password_reset_email(user, uid, token):
    """
    Sends a password reset email.
    """
    reset_url = f"http://localhost:8000/reset-password/{uid}/{token}/"
    send_mail(
        "Password Reset Requested",
        f"Please click the link to reset your password: {reset_url}",
        "no-reply@example.com",
        [user.email],
        fail_silently=False,
    )
    logger.info("Password reset link sent to %s", user.email)


def send_email_confirmation(user, new_email):
    """
    Send the email confirmation link to the new email address.
    """
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    confirmation_url = f"http://localhost:8000/confirm-email/{uid}/{token}/"

    subject = "Confirm your email address"
    message = f"Please confirm your email address by clicking the following link: {confirmation_url}"
    email_from = "no-reply@example.com"

    send_mail(subject, message, email_from, [new_email], fail_silently=False)
