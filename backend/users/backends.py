"""Custom authentication backend for Django admin."""

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailBackend(ModelBackend):
    """Custom backend to allow login with email instead of username."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        """Authenticate using email field."""
        UserModel = get_user_model()
        
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        
        if username is None or password is None:
            return None
        
        try:
            # Try to authenticate with email (case-insensitive)
            user = UserModel.objects.get(email__iexact=username)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user
            UserModel().set_password(password)
            return None
        except UserModel.MultipleObjectsReturned:
            # Handle the case where there are multiple users with the same email
            return None

        # Check password and if user can authenticate
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None

    def get_user(self, user_id):
        """Get user by ID."""
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
