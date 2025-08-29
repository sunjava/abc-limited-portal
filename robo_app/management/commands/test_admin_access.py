from django.core.management.base import BaseCommand
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse

class Command(BaseCommand):
    help = 'Test admin access and regular login'

    def handle(self, *args, **options):
        username = 'sm'
        password = 'sunjava@123'
        
        # Check user exists and has admin privileges
        try:
            user = User.objects.get(username=username)
            self.stdout.write(f"✅ User '{username}' exists")
            self.stdout.write(f"   - Is active: {user.is_active}")
            self.stdout.write(f"   - Is staff: {user.is_staff}")
            self.stdout.write(f"   - Is superuser: {user.is_superuser}")
            
            if not user.is_staff:
                self.stdout.write("❌ User is not staff - cannot access admin")
                return
                
        except User.DoesNotExist:
            self.stdout.write(f"❌ User '{username}' not found")
            return
            
        # Create test client
        client = Client()
        
        # Test 1: Regular login page
        self.stdout.write("\n--- Testing Regular Login ---")
        response = client.get('/login/')
        self.stdout.write(f"GET /login/ status: {response.status_code}")
        
        # Test 2: Admin login page
        self.stdout.write("\n--- Testing Admin Access ---")
        response = client.get('/admin/')
        self.stdout.write(f"GET /admin/ status: {response.status_code}")
        
        if response.status_code == 302:
            self.stdout.write("Admin redirects to login (normal behavior)")
        elif response.status_code == 200:
            self.stdout.write("Admin page accessible")
        else:
            self.stdout.write(f"Unexpected admin status: {response.status_code}")
            
        # Test 3: Admin login
        self.stdout.write("\n--- Testing Admin Login ---")
        response = client.get('/admin/login/')
        self.stdout.write(f"GET /admin/login/ status: {response.status_code}")
        
        # Test 4: Post login to admin
        if response.status_code == 200:
            # Get CSRF token from admin login page
            csrf_token = None
            content = response.content.decode('utf-8')
            if 'csrfmiddlewaretoken' in content:
                import re
                csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]*)"', content)
                if csrf_match:
                    csrf_token = csrf_match.group(1)
                    
            login_data = {
                'username': username,
                'password': password,
                'next': '/admin/',
            }
            if csrf_token:
                login_data['csrfmiddlewaretoken'] = csrf_token
                
            response = client.post('/admin/login/', login_data, follow=True)
            self.stdout.write(f"POST /admin/login/ status: {response.status_code}")
            self.stdout.write(f"Final URL: {response.request.get('PATH_INFO', 'Unknown')}")
            
            if 'admin' in response.request.get('PATH_INFO', '') and response.status_code == 200:
                self.stdout.write("✅ Successfully logged into admin")
            else:
                self.stdout.write("❌ Admin login failed")
                
        # Test 5: Regular app login
        self.stdout.write("\n--- Testing Regular App Login ---")
        client2 = Client()  # Fresh client
        response = client2.get('/login/')
        if response.status_code == 200:
            # Get CSRF token
            csrf_token = None
            content = response.content.decode('utf-8')
            if 'csrfmiddlewaretoken' in content:
                import re
                csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]*)"', content)
                if csrf_match:
                    csrf_token = csrf_match.group(1)
                    
            login_data = {
                'username': username,
                'password': password,
            }
            if csrf_token:
                login_data['csrfmiddlewaretoken'] = csrf_token
                
            response = client2.post('/login/', login_data, follow=True)
            self.stdout.write(f"POST /login/ status: {response.status_code}")
            self.stdout.write(f"Final URL: {response.request.get('PATH_INFO', 'Unknown')}")
            
            if 'dashboard' in response.request.get('PATH_INFO', '') or response.request.get('PATH_INFO', '') == '/':
                self.stdout.write("✅ Successfully logged into main app")
            else:
                self.stdout.write("❌ Main app login failed")
        else:
            self.stdout.write(f"❌ Cannot access login page: {response.status_code}")
