"""Serializers for Timeline app."""

from rest_framework import serializers
from .models import Timeline, TimelineEvent


class TimelineEventSerializer(serializers.ModelSerializer):
    """Serializer for TimelineEvent model."""
    
    created_by_email = serializers.CharField(source='created_by.email', read_only=True)
    timeline_title = serializers.CharField(source='timeline.title', read_only=True)
    
    class Meta:
        model = TimelineEvent
        fields = [
            'id',
            'timeline',
            'timeline_title',
            'title',
            'description',
            'event_date',
            'location',
            'attendees_count',
            'image',
            'created_by',
            'created_by_email',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']


class TimelineSerializer(serializers.ModelSerializer):
    """Serializer for Timeline model."""
    
    events = TimelineEventSerializer(many=True, read_only=True)
    events_count = serializers.SerializerMethodField()
    created_by_email = serializers.CharField(source='created_by.email', read_only=True)
    
    class Meta:
        model = Timeline
        fields = [
            'id',
            'title',
            'description',
            'category',
            'start_date',
            'end_date',
            'cover_image',
            'is_published',
            'is_featured',
            'events',
            'events_count',
            'created_by',
            'created_by_email',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at', 'events']
    
    def get_events_count(self, obj):
        """Get the count of events in the timeline."""
        return obj.events.count()
