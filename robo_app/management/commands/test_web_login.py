from django.core.management.base import BaseCommand
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse

class Command(BaseCommand):
    help = 'Test web login exactly like the browser would'

    def handle(self, *args, **options):
        username = 'sm'
        password = 'sunjava@123'
        
        # Check user exists
        try:
            user = User.objects.get(username=username)
            self.stdout.write(f"✅ User '{username}' exists")
            self.stdout.write(f"   - Is active: {user.is_active}")
            self.stdout.write(f"   - Is staff: {user.is_staff}")
            self.stdout.write(f"   - Is superuser: {user.is_superuser}")
        except User.DoesNotExist:
            self.stdout.write(f"❌ User '{username}' not found")
            return
            
        # Create test client
        client = Client()
        
        # Test GET request to login page
        self.stdout.write("\n--- Testing GET /login/ ---")
        response = client.get('/login/')
        self.stdout.write(f"Status code: {response.status_code}")
        if response.status_code == 200:
            self.stdout.write("✅ Login page loads successfully")
        else:
            self.stdout.write("❌ Login page failed to load")
            
        # Test POST request to login
        self.stdout.write("\n--- Testing POST /login/ ---")
        login_data = {
            'username': username,
            'password': password,
        }
        
        response = client.post('/login/', login_data, follow=True)
        self.stdout.write(f"Status code: {response.status_code}")
        self.stdout.write(f"Final URL: {response.request.get('PATH_INFO', 'Unknown')}")
        
        if response.status_code == 200:
            # Check if we're redirected to dashboard or still on login
            if 'login' in response.request.get('PATH_INFO', ''):
                self.stdout.write("❌ Still on login page - authentication failed")
                # Check for error messages
                content = response.content.decode('utf-8')
                if 'Invalid username or password' in content:
                    self.stdout.write("   - Error: Invalid username or password")
                elif 'error' in content.lower():
                    self.stdout.write("   - Some error message found in page")
            else:
                self.stdout.write("✅ Redirected away from login - likely successful")
                
        # Test direct authentication
        self.stdout.write("\n--- Testing Django Client Login ---")
        login_success = client.login(username=username, password=password)
        if login_success:
            self.stdout.write("✅ Django client.login() successful")
        else:
            self.stdout.write("❌ Django client.login() failed")
            
        # Test accessing protected page
        self.stdout.write("\n--- Testing Protected Page Access ---")
        response = client.get('/dashboard/')
        self.stdout.write(f"Dashboard access status: {response.status_code}")
        if response.status_code == 200:
            self.stdout.write("✅ Can access dashboard")
        elif response.status_code == 302:
            self.stdout.write("❌ Redirected (likely to login) - not authenticated")
        else:
            self.stdout.write(f"❌ Unexpected status: {response.status_code}")
