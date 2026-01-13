from django.contrib import admin
from .models import Timeline, TimelineEvent


@admin.register(Timeline)
class TimelineAdmin(admin.ModelAdmin):
    """Admin configuration for Timeline."""
    
    list_display = ('title', 'category', 'start_date', 'is_published', 'is_featured', 'created_by', 'created_at')
    list_filter = ('category', 'is_published', 'is_featured', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {'fields': ('title', 'description', 'category')}),
        ('Dates', {'fields': ('start_date', 'end_date')}),
        ('Media', {'fields': ('cover_image',)}),
        ('Status', {'fields': ('is_published', 'is_featured')}),
        ('Metadata', {'fields': ('created_by', 'created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    """Admin configuration for TimelineEvent."""
    
    list_display = ('title', 'timeline', 'event_date', 'location', 'attendees_count', 'created_at')
    list_filter = ('timeline', 'event_date', 'created_at')
    search_fields = ('title', 'description', 'location')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Event Information', {'fields': ('timeline', 'title', 'description')}),
        ('Event Details', {'fields': ('event_date', 'location', 'attendees_count')}),
        ('Media', {'fields': ('image',)}),
        ('Metadata', {'fields': ('created_by', 'created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
