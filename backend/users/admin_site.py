"""Custom admin site for email-based authentication."""

from django.contrib.admin import AdminSite
from django.contrib.auth.forms import AuthenticationForm
from django import forms


class EmailAuthenticationForm(AuthenticationForm):
    """Custom authentication form that uses email instead of username."""
    
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'autofocus': True}),
        label="Email"
    )


class CustomAdminSite(AdminSite):
    """Custom admin site that uses email for authentication."""
    
    site_header = "Versity Farewell Administration"
    site_title = "Versity Farewell Admin"
    index_title = "Welcome to Versity Farewell Administration"
    
    login_form = EmailAuthenticationForm
    
    def has_permission(self, request):
        """
        Check if the user has permission to access the admin site.
        """
        return request.user.is_active and request.user.is_staff


# Create an instance of our custom admin site
admin_site = CustomAdminSite(name='custom_admin')
