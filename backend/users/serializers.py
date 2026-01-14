from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import CustomUser, UserProfile, EmailVerificationToken
import uuid
from datetime import timedelta


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model."""
    
    class Meta:
        model = UserProfile
        fields = [
            'phone_number',
            'date_of_birth',
            'admission_year',
            'graduation_year',
            'branch',
            'roll_number',
            'notification_email',
            'notification_push',
        ]


class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer for CustomUser model."""
    
    profile = UserProfileSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'role',
            'is_email_verified',
            'profile_picture',
            'bio',
            'profile',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_full_name(self, obj):
        """Get user's full name."""
        first_name = obj.first_name or ""
        last_name = obj.last_name or ""
        return f"{first_name} {last_name}".strip()


class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = CustomUser
        fields = [
            'email',
            'first_name',
            'last_name',
            'password',
            'password_confirm',
        ]
    
    def validate(self, data):
        """Validate that passwords match."""
        if data['password'] != data.pop('password_confirm'):
            raise serializers.ValidationError("Passwords don't match.")
        return data
    
    def validate_email(self, value):
        """Validate email uniqueness."""
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value.lower()
    
    def create(self, validated_data):
        """Create and return a new user."""
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(**validated_data, password=password)
        
        # UserProfile is automatically created by the post_save signal
        # No need to create it explicitly here
        
        # Generate email verification token
        token = str(uuid.uuid4())
        expires_at = timezone.now() + timedelta(hours=24)
        EmailVerificationToken.objects.create(
            user=user,
            token=token,
            expires_at=expires_at
        )
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, data):
        """Authenticate user."""
        email = data.get('email', '').lower()
        password = data.get('password', '')
        
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")
        
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password.")
        
        if not user.is_active:
            raise serializers.ValidationError("This account is inactive.")
        
        data['user'] = user
        return data


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing password."""
    
    old_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    new_password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    
    def validate(self, data):
        """Validate passwords."""
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match.")
        
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError("New password must be different from the old password.")
        
        return data


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile."""
    
    profile = UserProfileSerializer(required=False)
    
    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'profile_picture',
            'bio',
            'profile',
        ]
    
    def update(self, instance, validated_data):
        """Update user and profile."""
        profile_data = validated_data.pop('profile', None)
        
        # Update user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update profile fields if provided
        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        
        return instance


class EmailVerificationSerializer(serializers.Serializer):
    """Serializer for email verification."""
    
    token = serializers.CharField(required=True)
    
    def validate_token(self, value):
        """Validate email verification token."""
        try:
            verification_token = EmailVerificationToken.objects.get(token=value)
        except EmailVerificationToken.DoesNotExist:
            raise serializers.ValidationError("Invalid verification token.")
        
        if not verification_token.is_valid():
            raise serializers.ValidationError("Verification token has expired or already used.")
        
        return verification_token
