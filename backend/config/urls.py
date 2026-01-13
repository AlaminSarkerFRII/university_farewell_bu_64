"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from users.views import AuthViewSet, UserViewSet, UserProfileViewSet
from timeline.views import TimelineViewSet, TimelineEventViewSet
from responsibilities.views import ResponsibilityViewSet, ResponsibilityCategoryViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'timelines', TimelineViewSet, basename='timeline')
router.register(r'timeline-events', TimelineEventViewSet, basename='timeline-event')
router.register(r'responsibilities', ResponsibilityViewSet, basename='responsibility')
router.register(r'responsibility-categories', ResponsibilityCategoryViewSet, basename='responsibility-category')

# Auth router (for special endpoints)
auth_router = DefaultRouter()
auth_router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include(auth_router.urls)),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Swagger/OpenAPI Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
