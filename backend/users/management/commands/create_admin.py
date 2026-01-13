"""Management command to create an admin user."""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    """Create an admin user for Django admin panel."""
    
    help = 'Create an admin user with email and password'
    
    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Admin email address')
        parser.add_argument('--password', type=str, help='Admin password')
        parser.add_argument('--first_name', type=str, help='Admin first name', default='Admin')
        parser.add_argument('--last_name', type=str, help='Admin last name', default='User')
    
    def handle(self, *args, **options):
        User = get_user_model()
        
        email = options.get('email')
        password = options.get('password')
        first_name = options.get('first_name')
        last_name = options.get('last_name')
        
        # If email or password not provided, use defaults
        if not email:
            email = 'admin@example.com'
            self.stdout.write(self.style.WARNING(f'No email provided, using default: {email}'))
        
        if not password:
            password = 'admin123456'
            self.stdout.write(self.style.WARNING('No password provided, using default: admin123456'))
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR(f'User with email {email} already exists!'))
            return
        
        # Create superuser
        try:
            user = User.objects.create_superuser(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            self.stdout.write(self.style.SUCCESS('=' * 60))
            self.stdout.write(self.style.SUCCESS('Admin user created successfully!'))
            self.stdout.write(self.style.SUCCESS('=' * 60))
            self.stdout.write(self.style.SUCCESS(f'Email: {email}'))
            self.stdout.write(self.style.SUCCESS(f'Password: {password}'))
            self.stdout.write(self.style.SUCCESS(f'Role: {user.role}'))
            self.stdout.write(self.style.SUCCESS(f'Is Staff: {user.is_staff}'))
            self.stdout.write(self.style.SUCCESS(f'Is Superuser: {user.is_superuser}'))
            self.stdout.write(self.style.SUCCESS('=' * 60))
            self.stdout.write(self.style.SUCCESS(f'Login at: http://localhost:8000/admin/'))
            self.stdout.write(self.style.SUCCESS('=' * 60))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating admin user: {str(e)}'))
