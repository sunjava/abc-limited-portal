from django.core.management.base import BaseCommand
from django.test import Client
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Test login redirect behavior'

    def handle(self, *args, **options):
        username = 'sm'
        password = 'sunjava@123'
        
        # Create test client
        client = Client()
        
        # Get login page and extract CSRF token
        self.stdout.write("--- Getting CSRF token ---")
        response = client.get('/login/')
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            # Extract CSRF token
            csrf_token = None
            import re
            csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]*)"', content)
            if csrf_match:
                csrf_token = csrf_match.group(1)
                
            # Test POST login with follow=True to see full redirect chain
            post_data = {
                'username': username,
                'password': password,
            }
            if csrf_token:
                post_data['csrfmiddlewaretoken'] = csrf_token
                
            self.stdout.write("--- Testing login with redirect following ---")
            response = client.post('/login/', post_data, follow=True)
            
            self.stdout.write(f"Final status code: {response.status_code}")
            self.stdout.write(f"Redirect chain:")
            for redirect in response.redirect_chain:
                self.stdout.write(f"  -> {redirect[0]} ({redirect[1]})")
                
            final_url = response.request.get('PATH_INFO', 'Unknown')
            self.stdout.write(f"Final URL: {final_url}")
            
            # Check if we ended up on dashboard
            if final_url == '/dashboard/' or final_url == '/':
                self.stdout.write("✅ Successfully redirected to dashboard")
                
                # Check if page contains dashboard content
                content = response.content.decode('utf-8')
                if 'Dashboard' in content or 'ABC Limited Portal' in content:
                    self.stdout.write("✅ Dashboard content loaded")
                else:
                    self.stdout.write("❌ Dashboard content not found")
                    
            elif 'login' in final_url:
                self.stdout.write("❌ Still on login page - authentication may have failed")
                
                # Check for error messages
                content = response.content.decode('utf-8')
                if 'Invalid username or password' in content:
                    self.stdout.write("  Error message: Invalid username or password")
                elif 'error' in content.lower():
                    self.stdout.write("  Some error found in page")
            else:
                self.stdout.write(f"⚠️  Unexpected final URL: {final_url}")
                
            # Test session after login
            self.stdout.write("\n--- Testing session after login ---")
            session_user_id = client.session.get('_auth_user_id')
            if session_user_id:
                self.stdout.write(f"✅ User ID in session: {session_user_id}")
            else:
                self.stdout.write("❌ No user ID in session")
                
            # Test accessing protected page
            self.stdout.write("\n--- Testing protected page access ---")
            dashboard_response = client.get('/dashboard/')
            self.stdout.write(f"Dashboard access status: {dashboard_response.status_code}")
            
            if dashboard_response.status_code == 200:
                self.stdout.write("✅ Can access dashboard after login")
            elif dashboard_response.status_code == 302:
                self.stdout.write("❌ Redirected from dashboard - session may not be working")
            else:
                self.stdout.write(f"⚠️  Unexpected dashboard status: {dashboard_response.status_code}")
                
        else:
            self.stdout.write(f"❌ Cannot access login page: {response.status_code}")
