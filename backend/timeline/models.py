from django.db import models
from users.models import CustomUser
import uuid


class Timeline(models.Model):
    """Timeline model for tracking farewell events."""
    
    CATEGORY_CHOICES = (
        ('admission', 'Admission'),
        ('academics', 'Academics'),
        ('events', 'Events'),
        ('placement', 'Placement'),
        ('preparation', 'Preparation'),
        ('farewell', 'Farewell'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Media
    cover_image = models.ImageField(upload_to='timeline_covers/', null=True, blank=True)
    
    # Status
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    # Metadata
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_timelines')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Timeline'
        verbose_name_plural = 'Timelines'
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['is_published']),
        ]
    
    def __str__(self):
        return self.title


class TimelineEvent(models.Model):
    """Individual event on a timeline."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timeline = models.ForeignKey(Timeline, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    event_date = models.DateField()
    
    # Event details
    location = models.CharField(max_length=200, blank=True)
    attendees_count = models.IntegerField(default=0)
    image = models.ImageField(upload_to='timeline_events/', null=True, blank=True)
    
    # Metadata
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Timeline Event'
        verbose_name_plural = 'Timeline Events'
        ordering = ['event_date']
        indexes = [
            models.Index(fields=['timeline', 'event_date']),
        ]
    
    def __str__(self):
        return f"{self.timeline.title} - {self.title}"
