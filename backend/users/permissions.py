"""Custom permission classes for role-based access control."""

from rest_framework.permissions import BasePermission


class IsOrganizer(BasePermission):
    """Permission class to check if user is an organizer."""
    
    message = "Only organizers can perform this action."
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['organizer', 'admin']
        )


class IsTreasurer(BasePermission):
    """Permission class to check if user is a treasurer."""
    
    message = "Only treasurers can perform this action."
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['treasurer', 'admin']
        )


class IsAdmin(BasePermission):
    """Permission class to check if user is an admin."""
    
    message = "Only admins can perform this action."
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'admin'
        )


class IsStudent(BasePermission):
    """Permission class to check if user is a student."""
    
    message = "Only students can perform this action."
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'student'
        )


class IsOwnerOrReadOnly(BasePermission):
    """Permission to allow owners to edit their own object."""
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # Write permissions are only allowed to the owner
        return obj.id == request.user.id or request.user.role == 'admin'


class IsOrganizerOrAdmin(BasePermission):
    """Permission class for organizer or admin access."""
    
    message = "Only organizers and admins can perform this action."
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['organizer', 'admin']
        )
