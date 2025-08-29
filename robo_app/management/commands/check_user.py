from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Check if user sm exists and can authenticate'

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username='sm')
            self.stdout.write(f"✅ User 'sm' exists")
            self.stdout.write(f"Email: {user.email}")
            self.stdout.write(f"First name: {user.first_name}")
            self.stdout.write(f"Last name: {user.last_name}")
            self.stdout.write(f"Is active: {user.is_active}")
            self.stdout.write(f"Is staff: {user.is_staff}")
            
            # Test password
            can_auth = user.check_password('sunjava@123')
            self.stdout.write(f"Can authenticate with 'sunjava@123': {can_auth}")
            
        except User.DoesNotExist:
            self.stdout.write("❌ User 'sm' does not exist")
            
            # Show all users
            all_users = User.objects.all()
            self.stdout.write(f"Total users in database: {all_users.count()}")
            for user in all_users:
                self.stdout.write(f"  - {user.username} ({user.email})")
