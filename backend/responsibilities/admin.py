from django.contrib import admin
from .models import ResponsibilityCategory, Responsibility, ResponsibilityRole


@admin.register(ResponsibilityCategory)
class ResponsibilityCategoryAdmin(admin.ModelAdmin):
    """Admin configuration for ResponsibilityCategory."""
    
    list_display = ('name', 'color', 'description')
    search_fields = ('name', 'description')


@admin.register(Responsibility)
class ResponsibilityAdmin(admin.ModelAdmin):
    """Admin configuration for Responsibility."""
    
    list_display = ('title', 'status', 'priority', 'due_date', 'is_overdue', 'created_by', 'created_at')
    list_filter = ('status', 'priority', 'category', 'due_date', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('assigned_to',)
    
    fieldsets = (
        ('Task Information', {'fields': ('title', 'description', 'category')}),
        ('Assignment', {'fields': ('assigned_to', 'created_by')}),
        ('Status & Priority', {'fields': ('status', 'priority')}),
        ('Dates', {'fields': ('start_date', 'due_date', 'completed_date')}),
        ('Metadata', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(ResponsibilityRole)
class ResponsibilityRoleAdmin(admin.ModelAdmin):
    """Admin configuration for ResponsibilityRole."""
    
    list_display = ('responsibility', 'user', 'role_type', 'created_at')
    list_filter = ('role_type', 'created_at')
    search_fields = ('responsibility__title', 'user__email')
