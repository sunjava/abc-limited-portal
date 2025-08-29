from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class Command(BaseCommand):
    help = 'Make sm user a superuser'

    def handle(self, *args, **options):
        username = 'sm'
        password = 'sunjava@123'
        
        try:
            user = User.objects.get(username=username)
            self.stdout.write(f"Found user '{username}'")
            
            # Configure as superuser
            user.is_active = True
            user.is_staff = True
            user.is_superuser = True
            user.email = 'sm@example.com'
            user.first_name = 'System'
            user.last_name = 'Manager'
            
            # Ensure password is correct
            user.set_password(password)
            user.save()
            
            self.stdout.write("✅ User updated to superuser:")
            self.stdout.write(f"  - Is active: {user.is_active}")
            self.stdout.write(f"  - Is staff: {user.is_staff}")
            self.stdout.write(f"  - Is superuser: {user.is_superuser}")
            
            # Test authentication
            auth_user = authenticate(username=username, password=password)
            if auth_user:
                self.stdout.write("✅ Authentication test passed")
                self.stdout.write(f"Login credentials: username='{username}', password='{password}'")
                self.stdout.write("🔑 User now has full admin access")
            else:
                self.stdout.write("❌ Authentication test failed")
                
        except User.DoesNotExist:
            self.stdout.write(f"❌ User '{username}' not found")
