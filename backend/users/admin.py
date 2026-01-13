from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, UserProfile, EmailVerificationToken, Role


# Register with default admin site
@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """Admin configuration for CustomUser."""
    
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active', 'is_email_verified', 'created_at')
    list_filter = ('role', 'is_active', 'is_email_verified', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    
    # Use email instead of username for authentication
    username_field = 'email'
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'profile_picture', 'bio')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Role & Status', {'fields': ('role', 'is_email_verified')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at', 'last_login'), 'classes': ('collapse',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'role'),
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'last_login')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin configuration for UserProfile."""
    
    list_display = ('user', 'admission_year', 'graduation_year', 'branch', 'created_at')
    list_filter = ('admission_year', 'graduation_year', 'branch')
    search_fields = ('user__email', 'roll_number')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    """Admin configuration for EmailVerificationToken."""
    
    list_display = ('user', 'is_used', 'is_valid', 'created_at', 'expires_at')
    list_filter = ('is_used', 'created_at')
    search_fields = ('user__email', 'token')
    readonly_fields = ('created_at', 'token')


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """Admin configuration for Role."""
    
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at',)
