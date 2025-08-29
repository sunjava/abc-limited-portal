from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class Command(BaseCommand):
    help = 'Fix sm user to be a regular user with correct settings'

    def handle(self, *args, **options):
        username = 'sm'
        password = 'sunjava@123'
        
        try:
            user = User.objects.get(username=username)
            self.stdout.write(f"Found user '{username}'")
            
            # Configure as regular user
            user.is_active = True
            user.is_staff = False
            user.is_superuser = False
            user.email = 'sm@example.com'
            user.first_name = 'System'
            user.last_name = 'Manager'
            
            # Reset password to be sure
            user.set_password(password)
            user.save()
            
            self.stdout.write("✅ User configuration updated:")
            self.stdout.write(f"  - Is active: {user.is_active}")
            self.stdout.write(f"  - Is staff: {user.is_staff}")
            self.stdout.write(f"  - Is superuser: {user.is_superuser}")
            
            # Test authentication
            auth_user = authenticate(username=username, password=password)
            if auth_user:
                self.stdout.write("✅ Authentication test passed")
            else:
                self.stdout.write("❌ Authentication test failed")
                
        except User.DoesNotExist:
            self.stdout.write(f"❌ User '{username}' not found")
