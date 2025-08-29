from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class Command(BaseCommand):
    help = 'Test exact login scenario'

    def handle(self, *args, **options):
        # Test the exact scenario from the form
        username = 'sm'
        password = 'sunjava@123'
        
        self.stdout.write(f"Testing login with username='{username}' and password='{password}'")
        
        # Check user exists
        try:
            user = User.objects.get(username=username)
            self.stdout.write(f"✅ User found: {user.username}")
            self.stdout.write(f"   - Is active: {user.is_active}")
            self.stdout.write(f"   - Has password: {bool(user.password)}")
            
            # Test password directly
            password_valid = user.check_password(password)
            self.stdout.write(f"   - Password valid: {password_valid}")
            
            # Test authenticate
            auth_result = authenticate(username=username, password=password)
            self.stdout.write(f"   - Authenticate result: {auth_result}")
            
            if auth_result is None:
                self.stdout.write("❌ Authentication failed - checking possible causes:")
                
                # Check for whitespace issues
                if username != username.strip():
                    self.stdout.write("   - Username has whitespace")
                if password != password.strip():
                    self.stdout.write("   - Password has whitespace")
                    
                # Test with stripped values
                auth_result2 = authenticate(username=username.strip(), password=password.strip())
                self.stdout.write(f"   - Authenticate with stripped values: {auth_result2}")
                
        except User.DoesNotExist:
            self.stdout.write(f"❌ User '{username}' not found")
            
        # Also test creating a brand new user for comparison
        test_username = 'testlogin'
        test_password = 'testpass123'
        
        # Delete if exists
        User.objects.filter(username=test_username).delete()
        
        # Create new test user
        test_user = User.objects.create_user(
            username=test_username,
            password=test_password,
            email='test@example.com'
        )
        
        # Test authenticate with new user
        auth_test = authenticate(username=test_username, password=test_password)
        self.stdout.write(f"\nTest with new user '{test_username}':")
        self.stdout.write(f"   - Authenticate result: {auth_test}")
        
        # Clean up
        test_user.delete()
