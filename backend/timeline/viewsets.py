"""API Views for Timeline app."""

from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Timeline, TimelineEvent
from .serializers import TimelineSerializer, TimelineEventSerializer
from users.permissions import IsOrganizerOrAdmin


class TimelineViewSet(viewsets.ModelViewSet):
    """ViewSet for Timeline CRUD operations."""
    
    queryset = Timeline.objects.all()
    serializer_class = TimelineSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_published', 'is_featured']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'start_date', 'end_date']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """Custom permissions based on action."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOrganizerOrAdmin()]
        return [permissions.IsAuthenticated()]
    
    def perform_create(self, serializer):
        """Create timeline with current user."""
        serializer.save(created_by=self.request.user)
    
    def get_queryset(self):
        """Filter timelines based on publication status."""
        user = self.request.user
        if user.role in ['admin', 'organizer']:
            return Timeline.objects.all()
        # Students only see published timelines
        return Timeline.objects.filter(is_published=True)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsOrganizerOrAdmin])
    def publish(self, request, pk=None):
        """Publish a timeline."""
        timeline = self.get_object()
        timeline.is_published = True
        timeline.save()
        return Response({'message': 'Timeline published'})
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsOrganizerOrAdmin])
    def unpublish(self, request, pk=None):
        """Unpublish a timeline."""
        timeline = self.get_object()
        timeline.is_published = False
        timeline.save()
        return Response({'message': 'Timeline unpublished'})
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsOrganizerOrAdmin])
    def feature(self, request, pk=None):
        """Feature a timeline."""
        timeline = self.get_object()
        timeline.is_featured = True
        timeline.save()
        return Response({'message': 'Timeline featured'})
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsOrganizerOrAdmin])
    def unfeature(self, request, pk=None):
        """Unfeature a timeline."""
        timeline = self.get_object()
        timeline.is_featured = False
        timeline.save()
        return Response({'message': 'Timeline unfeatured'})
    
    @action(detail=True, methods=['get'])
    def events(self, request, pk=None):
        """Get all events for a timeline."""
        timeline = self.get_object()
        events = timeline.events.all()
        serializer = TimelineEventSerializer(events, many=True)
        return Response(serializer.data)


class TimelineEventViewSet(viewsets.ModelViewSet):
    """ViewSet for Timeline Event CRUD operations."""
    
    queryset = TimelineEvent.objects.all()
    serializer_class = TimelineEventSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['timeline', 'event_date']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['event_date', 'created_at']
    ordering = ['event_date']
    
    def get_permissions(self):
        """Custom permissions based on action."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOrganizerOrAdmin()]
        return [permissions.IsAuthenticated()]
    
    def perform_create(self, serializer):
        """Create event with current user."""
        serializer.save(created_by=self.request.user)
    
    def get_queryset(self):
        """Filter events based on timeline permissions."""
        user = self.request.user
        if user.role in ['admin', 'organizer']:
            return TimelineEvent.objects.all()
        # Students only see events from published timelines
        return TimelineEvent.objects.filter(timeline__is_published=True)
