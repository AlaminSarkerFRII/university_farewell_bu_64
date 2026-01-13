"""API Views for Responsibilities app."""

from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Responsibility, ResponsibilityCategory
from .serializers import ResponsibilitySerializer, ResponsibilityCategorySerializer
from users.permissions import IsOrganizerOrAdmin


class ResponsibilityViewSet(viewsets.ModelViewSet):
    """ViewSet for Responsibility CRUD operations."""
    queryset = Responsibility.objects.all()
    serializer_class = ResponsibilitySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'priority', 'status', 'assigned_to']
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'priority', 'created_at']
    ordering = ['due_date']
    
    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [permissions.IsAuthenticated(), IsOrganizerOrAdmin()]
        return [permissions.IsAuthenticated()]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Responsibility.objects.all()
        if user.role in ['organizer', 'treasurer']:
            return Responsibility.objects.all()
        return Responsibility.objects.filter(assigned_to=user)
    
    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def update_status(self, request, pk=None):
        responsibility = self.get_object()
        new_status = request.data.get('status')
        valid_statuses = ['pending', 'in_progress', 'completed', 'on_hold']
        if new_status not in valid_statuses:
            return Response({'error': f'Invalid status. Choose from: {", ".join(valid_statuses)}'}, status=status.HTTP_400_BAD_REQUEST)
        responsibility.status = new_status
        responsibility.save()
        return Response(ResponsibilitySerializer(responsibility).data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsOrganizerOrAdmin])
    def assign_to(self, request, pk=None):
        from users.models import CustomUser
        responsibility = self.get_object()
        user_id = request.data.get('user_id')
        try:
            user = CustomUser.objects.get(id=user_id)
            responsibility.assigned_to = user
            responsibility.save()
            return Response(ResponsibilitySerializer(responsibility).data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_responsibilities(self, request):
        responsibilities = Responsibility.objects.filter(assigned_to=request.user)
        serializer = self.get_serializer(responsibilities, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        statuses = ['pending', 'in_progress', 'completed', 'on_hold']
        result = {}
        for status_choice in statuses:
            responsibilities = self.get_queryset().filter(status=status_choice)
            result[status_choice] = ResponsibilitySerializer(responsibilities, many=True).data
        return Response(result)
    
    @action(detail=False, methods=['get'])
    def by_priority(self, request):
        priorities = ['low', 'medium', 'high', 'urgent']
        result = {}
        for priority in priorities:
            responsibilities = self.get_queryset().filter(priority=priority)
            result[priority] = ResponsibilitySerializer(responsibilities, many=True).data
        return Response(result)


class ResponsibilityCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for Responsibility Category CRUD operations."""
    queryset = ResponsibilityCategory.objects.all()
    serializer_class = ResponsibilityCategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsOrganizerOrAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
    
    def get_permissions(self):
        if self.action == 'list':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsOrganizerOrAdmin()]
