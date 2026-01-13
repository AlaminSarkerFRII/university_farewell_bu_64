"""Serializers for Responsibilities app."""

from rest_framework import serializers
from .models import Responsibility, ResponsibilityCategory


class ResponsibilityCategorySerializer(serializers.ModelSerializer):
    """Serializer for ResponsibilityCategory model."""
    
    class Meta:
        model = ResponsibilityCategory
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class ResponsibilitySerializer(serializers.ModelSerializer):
    """Serializer for Responsibility model."""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    assigned_to_email = serializers.CharField(source='assigned_to.email', read_only=True, allow_null=True)
    created_by_email = serializers.CharField(source='created_by.email', read_only=True)
    
    class Meta:
        model = Responsibility
        fields = [
            'id',
            'title',
            'description',
            'category',
            'category_name',
            'priority',
            'status',
            'assigned_to',
            'assigned_to_email',
            'due_date',
            'created_by',
            'created_by_email',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
