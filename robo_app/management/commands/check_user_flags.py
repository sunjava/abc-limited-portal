from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Check user flags for sm user'

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username='sm')
            self.stdout.write(f"User 'sm' details:")
            self.stdout.write(f"  - Username: {user.username}")
            self.stdout.write(f"  - Email: {user.email}")
            self.stdout.write(f"  - First name: {user.first_name}")
            self.stdout.write(f"  - Last name: {user.last_name}")
            self.stdout.write(f"  - Is active: {user.is_active}")
            self.stdout.write(f"  - Is staff: {user.is_staff}")
            self.stdout.write(f"  - Is superuser: {user.is_superuser}")
            self.stdout.write(f"  - Date joined: {user.date_joined}")
            self.stdout.write(f"  - Last login: {user.last_login}")
            
            # Fix the user if needed
            if not user.is_active:
                user.is_active = True
                user.save()
                self.stdout.write("✅ Fixed: Set user to active")
                
            # Ensure staff is False (regular user)
            if user.is_staff:
                user.is_staff = False
                user.save()
                self.stdout.write("✅ Fixed: Removed staff privileges")
                
        except User.DoesNotExist:
            self.stdout.write("❌ User 'sm' does not exist")
