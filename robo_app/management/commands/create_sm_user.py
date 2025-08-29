from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create or update the sm user with correct password'

    def handle(self, *args, **options):
        username = 'sm'
        password = 'sunjava@123'
        email = 'sm@example.com'
        
        try:
            # Try to get existing user
            user = User.objects.get(username=username)
            self.stdout.write(f"User '{username}' already exists. Updating password...")
            user.set_password(password)
            user.email = email
            user.is_active = True
            user.save()
            self.stdout.write(f"✅ Updated user '{username}' with new password")
            
        except User.DoesNotExist:
            # Create new user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name='System',
                last_name='Manager'
            )
            user.is_active = True
            user.save()
            self.stdout.write(f"✅ Created new user '{username}'")
        
        # Test authentication
        can_auth = user.check_password(password)
        self.stdout.write(f"Password check result: {can_auth}")
        self.stdout.write(f"User is active: {user.is_active}")
        self.stdout.write(f"Login credentials: username='{username}', password='{password}'")
