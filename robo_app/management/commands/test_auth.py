from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Test authentication for user sm'

    def handle(self, *args, **options):
        username = 'sm'
        password = 'sunjava@123'
        
        # Check if user exists
        try:
            user = User.objects.get(username=username)
            self.stdout.write(f"✅ User '{username}' exists")
            self.stdout.write(f"   - Email: {user.email}")
            self.stdout.write(f"   - Is active: {user.is_active}")
            self.stdout.write(f"   - Is staff: {user.is_staff}")
            self.stdout.write(f"   - Date joined: {user.date_joined}")
            
            # Test password check
            password_ok = user.check_password(password)
            self.stdout.write(f"   - Password check: {password_ok}")
            
            # Test Django authenticate function
            auth_user = authenticate(username=username, password=password)
            if auth_user:
                self.stdout.write(f"✅ Django authenticate() successful")
                self.stdout.write(f"   - Authenticated user: {auth_user.username}")
            else:
                self.stdout.write(f"❌ Django authenticate() failed")
                
                # Check if user is active
                if not user.is_active:
                    self.stdout.write("   - Reason: User is not active")
                else:
                    self.stdout.write("   - Reason: Unknown (user exists and is active)")
                    
        except User.DoesNotExist:
            self.stdout.write(f"❌ User '{username}' does not exist")
            
        # List all users for debugging
        self.stdout.write("\n--- All users in database ---")
        for user in User.objects.all():
            self.stdout.write(f"Username: {user.username}, Active: {user.is_active}, Email: {user.email}")
