from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend

class Command(BaseCommand):
    help = 'Deep debug of authentication process'

    def handle(self, *args, **options):
        username = 'sm'
        password = 'sunjava@123'
        
        self.stdout.write("=== DEEP AUTHENTICATION DEBUG ===\n")
        
        # Step 1: Check if user exists
        self.stdout.write("1. Checking user existence:")
        try:
            user = User.objects.get(username=username)
            self.stdout.write(f"   ✅ User found: {user.username}")
            self.stdout.write(f"   - ID: {user.id}")
            self.stdout.write(f"   - Email: {user.email}")
            self.stdout.write(f"   - Is active: {user.is_active}")
            self.stdout.write(f"   - Is staff: {user.is_staff}")
            self.stdout.write(f"   - Is superuser: {user.is_superuser}")
            self.stdout.write(f"   - Date joined: {user.date_joined}")
            self.stdout.write(f"   - Last login: {user.last_login}")
            self.stdout.write(f"   - Password hash: {user.password[:50]}...")
        except User.DoesNotExist:
            self.stdout.write("   ❌ User does not exist")
            return
            
        # Step 2: Test password directly
        self.stdout.write("\n2. Testing password directly:")
        password_valid = user.check_password(password)
        self.stdout.write(f"   Password check result: {password_valid}")
        
        if not password_valid:
            self.stdout.write("   ❌ Password check failed!")
            # Try different password variations
            test_passwords = [
                'sunjava@123',
                'sunjava123',
                'Sunjava@123',
                'SUNJAVA@123',
            ]
            self.stdout.write("   Trying password variations:")
            for test_pwd in test_passwords:
                result = user.check_password(test_pwd)
                self.stdout.write(f"   - '{test_pwd}': {result}")
                
        # Step 3: Test authentication backends
        self.stdout.write("\n3. Testing authentication backends:")
        from django.conf import settings
        
        # Get authentication backends
        backends = getattr(settings, 'AUTHENTICATION_BACKENDS', ['django.contrib.auth.backends.ModelBackend'])
        self.stdout.write(f"   Configured backends: {backends}")
        
        # Test each backend
        for backend_path in backends:
            self.stdout.write(f"\n   Testing backend: {backend_path}")
            try:
                # Import the backend
                module_name, class_name = backend_path.rsplit('.', 1)
                module = __import__(module_name, fromlist=[class_name])
                backend_class = getattr(module, class_name)
                backend = backend_class()
                
                # Test authentication
                auth_result = backend.authenticate(None, username=username, password=password)
                self.stdout.write(f"   - Result: {auth_result}")
                
                if auth_result:
                    self.stdout.write(f"   - Authenticated user: {auth_result.username}")
                else:
                    self.stdout.write("   - Authentication failed")
                    
            except Exception as e:
                self.stdout.write(f"   - Error: {str(e)}")
                
        # Step 4: Test Django's authenticate function
        self.stdout.write("\n4. Testing Django's authenticate function:")
        auth_user = authenticate(username=username, password=password)
        self.stdout.write(f"   Result: {auth_user}")
        
        if auth_user:
            self.stdout.write(f"   ✅ Django authenticate successful: {auth_user.username}")
        else:
            self.stdout.write("   ❌ Django authenticate failed")
            
        # Step 5: Check if there are multiple users with same username
        self.stdout.write("\n5. Checking for duplicate usernames:")
        users_with_name = User.objects.filter(username=username)
        self.stdout.write(f"   Users found: {users_with_name.count()}")
        for i, u in enumerate(users_with_name):
            self.stdout.write(f"   User {i+1}: ID={u.id}, Active={u.is_active}, Password={u.password[:20]}...")
            
        # Step 6: Test case sensitivity
        self.stdout.write("\n6. Testing case sensitivity:")
        test_usernames = [username.lower(), username.upper(), username.title()]
        for test_user in test_usernames:
            if test_user != username:
                try:
                    alt_user = User.objects.get(username=test_user)
                    self.stdout.write(f"   Found user with username '{test_user}': {alt_user.id}")
                except User.DoesNotExist:
                    pass
                    
        # Step 7: Manual authentication simulation
        self.stdout.write("\n7. Manual authentication simulation:")
        try:
            # Get user
            user = User.objects.get(username=username)
            
            # Check if user is active
            if not user.is_active:
                self.stdout.write("   ❌ User is not active")
            else:
                self.stdout.write("   ✅ User is active")
                
            # Check password
            if user.check_password(password):
                self.stdout.write("   ✅ Password is correct")
                self.stdout.write("   🎯 Manual authentication would succeed")
            else:
                self.stdout.write("   ❌ Password is incorrect")
                
        except Exception as e:
            self.stdout.write(f"   Error in manual simulation: {str(e)}")
            
        self.stdout.write("\n=== END DEBUG ===")
