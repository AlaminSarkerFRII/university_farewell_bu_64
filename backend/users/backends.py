"""Custom authentication backend for Django admin."""

from django.contrib.auth.backends import ModelBackend
from users.models import CustomUser


class EmailBackend(ModelBackend):
    """Custom backend to allow login with email instead of username."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        """Authenticate using email field."""
        try:
            # Try to authenticate with email
            user = CustomUser.objects.get(email=username)
        except CustomUser.DoesNotExist:
            return None

        # Check password
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def get_user(self, user_id):
        """Get user by ID."""
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
