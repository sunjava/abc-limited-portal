from django.core.management.base import BaseCommand
from django.test import Client
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Debug what data is actually being sent in login form'

    def handle(self, *args, **options):
        username = 'sm'
        password = 'sunjava@123'
        
        # Create test client
        client = Client()
        
        # Get login page first to get CSRF token
        self.stdout.write("--- Getting login page for CSRF token ---")
        response = client.get('/login/')
        self.stdout.write(f"Login page status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            # Extract CSRF token
            csrf_token = None
            import re
            csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]*)"', content)
            if csrf_match:
                csrf_token = csrf_match.group(1)
                self.stdout.write(f"CSRF token found: {csrf_token[:20]}...")
            else:
                self.stdout.write("❌ No CSRF token found in login page")
                
            # Check form structure
            if 'name="username"' in content:
                self.stdout.write("✅ Username field found in form")
            else:
                self.stdout.write("❌ Username field NOT found in form")
                
            if 'name="password"' in content:
                self.stdout.write("✅ Password field found in form")
            else:
                self.stdout.write("❌ Password field NOT found in form")
                
            # Test different POST data formats
            self.stdout.write("\n--- Testing POST with different data formats ---")
            
            # Test 1: Basic POST data
            post_data_1 = {
                'username': username,
                'password': password,
            }
            if csrf_token:
                post_data_1['csrfmiddlewaretoken'] = csrf_token
                
            self.stdout.write(f"Test 1 - POST data: {post_data_1}")
            response1 = client.post('/login/', post_data_1)
            self.stdout.write(f"Response status: {response1.status_code}")
            
            # Test 2: URL encoded data
            import urllib.parse
            encoded_data = urllib.parse.urlencode(post_data_1)
            self.stdout.write(f"Test 2 - URL encoded: {encoded_data}")
            
            # Test 3: Check what the view actually receives
            self.stdout.write("\n--- Testing with manual request simulation ---")
            
            # Create a more detailed test
            from django.test import RequestFactory
            from robo_app.views import login_view
            from django.middleware.csrf import get_token
            
            factory = RequestFactory()
            request = factory.post('/login/', post_data_1)
            request.session = {}
            
            # Add user to request (needed for some middleware)
            from django.contrib.auth.models import AnonymousUser
            request.user = AnonymousUser()
            
            self.stdout.write("Simulating direct view call...")
            try:
                # This will help us see what the view receives
                response = login_view(request)
                self.stdout.write(f"Direct view call status: {response.status_code}")
            except Exception as e:
                self.stdout.write(f"Direct view call error: {str(e)}")
                
        else:
            self.stdout.write("❌ Cannot get login page to test form data")
            
        # Also test if the user can authenticate at all
        self.stdout.write("\n--- Testing direct authentication ---")
        from django.contrib.auth import authenticate
        
        user = authenticate(username=username, password=password)
        if user:
            self.stdout.write("✅ Direct authentication works")
            self.stdout.write(f"User: {user.username}, Active: {user.is_active}")
        else:
            self.stdout.write("❌ Direct authentication failed")
            
            # Check if user exists
            try:
                user_obj = User.objects.get(username=username)
                self.stdout.write(f"User exists: {user_obj.username}")
                self.stdout.write(f"Password check: {user_obj.check_password(password)}")
            except User.DoesNotExist:
                self.stdout.write("User does not exist")
