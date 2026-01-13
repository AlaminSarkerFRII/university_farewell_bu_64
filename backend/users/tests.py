from django.test import TestCase
from users.models import CustomUser, UserProfile, EmailVerificationToken
from timeline.models import Timeline, TimelineEvent
from responsibilities.models import Responsibility, ResponsibilityCategory


class UserModelTests(TestCase):
    """Tests for User models."""
    
    def setUp(self):
        """Create test user."""
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
    
    def test_user_creation(self):
        """Test that user is created successfully."""
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))
        self.assertEqual(self.user.role, 'student')
    
    def test_user_profile_created(self):
        """Test that user profile is created with user."""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertEqual(self.user.profile.user, self.user)
    
    def test_user_methods(self):
        """Test user methods."""
        self.assertEqual(self.user.get_full_name(), 'Test User')
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_admin())
    
    def test_superuser_creation(self):
        """Test superuser creation."""
        admin = CustomUser.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123'
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertEqual(admin.role, 'admin')


class TimelineModelTests(TestCase):
    """Tests for Timeline models."""
    
    def setUp(self):
        """Create test timeline."""
        self.user = CustomUser.objects.create_user(
            email='organizer@example.com',
            password='testpass123'
        )
        self.timeline = Timeline.objects.create(
            title='Test Timeline',
            description='Test Description',
            category='admission',
            start_date='2024-01-01',
            end_date='2024-06-01',
            created_by=self.user
        )
    
    def test_timeline_creation(self):
        """Test timeline creation."""
        self.assertEqual(self.timeline.title, 'Test Timeline')
        self.assertEqual(self.timeline.category, 'admission')
        self.assertEqual(self.timeline.created_by, self.user)
    
    def test_timeline_event_creation(self):
        """Test timeline event creation."""
        event = TimelineEvent.objects.create(
            timeline=self.timeline,
            title='Test Event',
            event_date='2024-02-01',
            created_by=self.user
        )
        self.assertEqual(event.title, 'Test Event')
        self.assertEqual(event.timeline, self.timeline)


class ResponsibilityModelTests(TestCase):
    """Tests for Responsibility models."""
    
    def setUp(self):
        """Create test responsibility."""
        self.user = CustomUser.objects.create_user(
            email='organizer@example.com',
            password='testpass123'
        )
        self.category = ResponsibilityCategory.objects.create(
            name='Setup'
        )
        self.responsibility = Responsibility.objects.create(
            title='Arrange Venue',
            description='Find and book venue for event',
            category=self.category,
            priority='high',
            start_date='2024-01-01',
            due_date='2024-02-01',
            created_by=self.user
        )
        self.responsibility.assigned_to.add(self.user)
    
    def test_responsibility_creation(self):
        """Test responsibility creation."""
        self.assertEqual(self.responsibility.title, 'Arrange Venue')
        self.assertEqual(self.responsibility.status, 'pending')
        self.assertEqual(self.responsibility.priority, 'high')
    
    def test_responsibility_assignment(self):
        """Test responsibility assignment."""
        self.assertIn(self.user, self.responsibility.assigned_to.all())
