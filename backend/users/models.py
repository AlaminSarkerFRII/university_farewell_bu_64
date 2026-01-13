from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import EmailValidator
import uuid


class CustomUserManager(BaseUserManager):
    """Custom manager for the CustomUser model."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user."""
        if not email:
            raise ValueError('Email is required')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True')
        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True')
        
        return self.create_user(email, password, **extra_fields)


class Role(models.Model):
    """Role model for RBAC."""
    
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('organizer', 'Organizer'),
        ('treasurer', 'Treasurer'),
        ('admin', 'Admin'),
    )
    
    name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        ordering = ['name']
    
    def __str__(self):
        return self.get_name_display()


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom User model using email as username."""
    
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('organizer', 'Organizer'),
        ('treasurer', 'Treasurer'),
        ('admin', 'Admin'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    
    # User status
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    
    # Role-based access
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    
    # Profile information
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        """Return the user's full name."""
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_short_name(self):
        """Return the user's short name."""
        return self.first_name or self.email.split('@')[0]
    
    def is_organizer(self):
        """Check if user has organizer role."""
        return self.role in ['organizer', 'admin']
    
    def is_treasurer(self):
        """Check if user has treasurer role."""
        return self.role in ['treasurer', 'admin']
    
    def is_admin(self):
        """Check if user has admin role."""
        return self.role == 'admin'


class UserProfile(models.Model):
    """Extended user profile information."""
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    admission_year = models.IntegerField(null=True, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    branch = models.CharField(max_length=100, blank=True)
    roll_number = models.CharField(max_length=50, blank=True)
    
    # Preferences
    notification_email = models.BooleanField(default=True)
    notification_push = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"{self.user.email} Profile"


class EmailVerificationToken(models.Model):
    """Store email verification tokens."""
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='verification_token')
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Email Verification Token'
        verbose_name_plural = 'Email Verification Tokens'
    
    def __str__(self):
        return f"Token for {self.user.email}"
    
    def is_valid(self):
        """Check if token is still valid."""
        from django.utils import timezone
        return not self.is_used and self.expires_at > timezone.now()
