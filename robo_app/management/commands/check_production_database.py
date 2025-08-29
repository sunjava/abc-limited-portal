from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import connection

class Command(BaseCommand):
    help = 'Check what is actually in the production database'

    def handle(self, *args, **options):
        self.stdout.write("=== PRODUCTION DATABASE CHECK ===\n")
        
        # Check database connection
        self.stdout.write("1. Database Connection:")
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                self.stdout.write(f"   ✅ Database connection working: {result}")
        except Exception as e:
            self.stdout.write(f"   ❌ Database connection failed: {str(e)}")
            return
            
        # Check database name/info
        self.stdout.write("\n2. Database Info:")
        db_settings = connection.settings_dict
        self.stdout.write(f"   Engine: {db_settings.get('ENGINE', 'Unknown')}")
        self.stdout.write(f"   Name: {db_settings.get('NAME', 'Unknown')}")
        self.stdout.write(f"   Host: {db_settings.get('HOST', 'Unknown')}")
        self.stdout.write(f"   Port: {db_settings.get('PORT', 'Unknown')}")
        
        # Check if auth_user table exists
        self.stdout.write("\n3. Checking auth_user table:")
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM auth_user")
                user_count = cursor.fetchone()[0]
                self.stdout.write(f"   ✅ auth_user table exists with {user_count} users")
        except Exception as e:
            self.stdout.write(f"   ❌ auth_user table issue: {str(e)}")
            
        # List all users in database
        self.stdout.write("\n4. All users in database:")
        try:
            users = User.objects.all()
            self.stdout.write(f"   Total users: {users.count()}")
            
            if users.count() == 0:
                self.stdout.write("   ❌ NO USERS FOUND IN DATABASE!")
            else:
                for i, user in enumerate(users[:10], 1):  # Show first 10 users
                    self.stdout.write(f"   User {i}: '{user.username}' (ID: {user.id}, Active: {user.is_active})")
                    
                if users.count() > 10:
                    self.stdout.write(f"   ... and {users.count() - 10} more users")
                    
        except Exception as e:
            self.stdout.write(f"   ❌ Error querying users: {str(e)}")
            
        # Specifically check for 'sm' user
        self.stdout.write("\n5. Checking for 'sm' user specifically:")
        try:
            sm_user = User.objects.get(username='sm')
            self.stdout.write(f"   ✅ User 'sm' found!")
            self.stdout.write(f"   - ID: {sm_user.id}")
            self.stdout.write(f"   - Email: {sm_user.email}")
            self.stdout.write(f"   - Active: {sm_user.is_active}")
            self.stdout.write(f"   - Staff: {sm_user.is_staff}")
            self.stdout.write(f"   - Superuser: {sm_user.is_superuser}")
        except User.DoesNotExist:
            self.stdout.write("   ❌ User 'sm' NOT FOUND!")
        except Exception as e:
            self.stdout.write(f"   ❌ Error checking 'sm' user: {str(e)}")
            
        # Check for users with similar names
        self.stdout.write("\n6. Checking for similar usernames:")
        similar_names = ['SM', 'Sm', 'sM', 'admin', 'superuser', 'test', 'user']
        for name in similar_names:
            try:
                user = User.objects.get(username=name)
                self.stdout.write(f"   Found user: '{name}' (ID: {user.id})")
            except User.DoesNotExist:
                pass
            except Exception as e:
                self.stdout.write(f"   Error checking '{name}': {str(e)}")
                
        # Check raw database query
        self.stdout.write("\n7. Raw database query for 'sm':")
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, username, email, is_active FROM auth_user WHERE username = %s", ['sm'])
                result = cursor.fetchone()
                if result:
                    self.stdout.write(f"   ✅ Raw query found: ID={result[0]}, username='{result[1]}', email='{result[2]}', active={result[3]}")
                else:
                    self.stdout.write("   ❌ Raw query found NO results for 'sm'")
                    
                # Check all usernames in database
                cursor.execute("SELECT username FROM auth_user ORDER BY username")
                all_usernames = cursor.fetchall()
                self.stdout.write(f"   All usernames in database: {[u[0] for u in all_usernames]}")
                    
        except Exception as e:
            self.stdout.write(f"   ❌ Raw query error: {str(e)}")
            
        self.stdout.write("\n=== END DATABASE CHECK ===")
