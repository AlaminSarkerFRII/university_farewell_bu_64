from django.db import models
from users.models import CustomUser
import uuid


class ResponsibilityCategory(models.Model):
    """Categories for responsibilities."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#3498db')  # Hex color
    
    class Meta:
        verbose_name = 'Responsibility Category'
        verbose_name_plural = 'Responsibility Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Responsibility(models.Model):
    """Responsibility/Task model."""
    
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(ResponsibilityCategory, on_delete=models.SET_NULL, null=True, related_name='responsibilities')
    
    # Assignment and status
    assigned_to = models.ManyToManyField(CustomUser, related_name='assigned_responsibilities')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    # Dates
    start_date = models.DateField()
    due_date = models.DateField()
    completed_date = models.DateField(null=True, blank=True)
    
    # Metadata
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_responsibilities')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Responsibility'
        verbose_name_plural = 'Responsibilities'
        ordering = ['-priority', 'due_date']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['due_date']),
        ]
    
    def __str__(self):
        return self.title
    
    def is_overdue(self):
        """Check if responsibility is overdue."""
        from django.utils import timezone
        return self.due_date < timezone.now().date() and self.status != 'completed'


class ResponsibilityRole(models.Model):
    """Define roles for responsibilities (e.g., led, arranged, contributed)."""
    
    ROLE_TYPES = (
        ('led', 'Led'),
        ('arranged', 'Arranged'),
        ('contributed', 'Contributed'),
        ('supported', 'Supported'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    responsibility = models.ForeignKey(Responsibility, on_delete=models.CASCADE, related_name='roles')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    role_type = models.CharField(max_length=20, choices=ROLE_TYPES)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Responsibility Role'
        verbose_name_plural = 'Responsibility Roles'
        unique_together = ('responsibility', 'user', 'role_type')
    
    def __str__(self):
        return f"{self.user.email} - {self.get_role_type_display()} on {self.responsibility.title}"
