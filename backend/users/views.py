"""API Views for Users app."""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from .models import CustomUser, UserProfile
from .serializers import (
    CustomUserSerializer,
    UserProfileSerializer,
    UserRegisterSerializer,
    UserLoginSerializer,
    ChangePasswordSerializer,
    UserUpdateSerializer,
)
from .permissions import IsOrganizerOrAdmin, IsOwnerOrReadOnly


class AuthViewSet(viewsets.ViewSet):
    """ViewSet for authentication endpoints."""
    permission_classes = [permissions.AllowAny]
    
    @extend_schema(
        request=UserRegisterSerializer,
        responses={
            201: OpenApiResponse(
                response=CustomUserSerializer,
                description='User registered successfully'
            ),
            400: OpenApiResponse(description='Bad request - validation errors')
        },
        description='Register a new user with email and password',
        summary='Register new user',
        tags=['Authentication']
    )
    @action(detail=False, methods=['post'])
    def register(self, request):
        """Register new user."""
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'User registered successfully',
                'user': CustomUserSerializer(user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        request=UserLoginSerializer,
        responses={
            200: OpenApiResponse(
                response=CustomUserSerializer,
                description='Login successful'
            ),
            401: OpenApiResponse(description='Invalid credentials'),
            400: OpenApiResponse(description='Bad request - validation errors')
        },
        description='Login with email and password to get JWT tokens',
        summary='Login user',
        tags=['Authentication']
    )
    @action(detail=False, methods=['post'])
    def login(self, request):
        """Login and get JWT tokens."""
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(username=email, password=password)
            if user is None:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            if not user.is_active:
                return Response({'error': 'User disabled'}, status=status.HTTP_401_UNAUTHORIZED)
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login successful',
                'user': CustomUserSerializer(user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        request=None,
        responses={
            200: OpenApiResponse(description='Logout successful')
        },
        description='Logout user (token invalidation handled client-side)',
        summary='Logout user',
        tags=['Authentication']
    )
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    
    @extend_schema(
        request={'refresh': 'string'},
        responses={
            200: OpenApiResponse(description='Token refreshed successfully'),
            400: OpenApiResponse(description='Invalid refresh token')
        },
        description='Refresh JWT access token using refresh token',
        summary='Refresh access token',
        tags=['Authentication']
    )
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def refresh_token(self, request):
        try:
            refresh = RefreshToken(request.data.get('refresh'))
            return Response({'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        if self.request.user.role == 'admin':
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=self.request.user.id)
    
    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=CustomUserSerializer,
                description='Current user profile'
            )
        },
        description='Get current authenticated user profile',
        summary='Get user profile',
        tags=['User Profile']
    )
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def profile(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @extend_schema(
        request=UserUpdateSerializer,
        responses={
            200: OpenApiResponse(
                response=UserUpdateSerializer,
                description='Profile updated successfully'
            ),
            400: OpenApiResponse(description='Bad request - validation errors')
        },
        description='Update current user profile',
        summary='Update user profile',
        tags=['User Profile']
    )
    @action(detail=False, methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def update_profile(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        request=ChangePasswordSerializer,
        responses={
            200: OpenApiResponse(description='Password changed successfully'),
            400: OpenApiResponse(description='Bad request - validation errors')
        },
        description='Change password for current user',
        summary='Change password',
        tags=['User Profile']
    )
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'old_password': 'Wrong password'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Password changed successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role == 'admin':
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=self.request.user)
