from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from robo_app.models import Account, Line, Service, LineService
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Set up production data including test user and sample accounts'

    def handle(self, *args, **options):
        # Create test user
        if not User.objects.filter(username='sm').exists():
            user = User.objects.create_user(
                username='sm',
                email='sm@example.com',
                password='sunjava@123',
                first_name='System',
                last_name='Manager'
            )
            self.stdout.write(f"Created user: {user.username}")
        else:
            self.stdout.write("User 'sm' already exists")

        # Create services if they don't exist
        services_data = [
            {'name': 'Unlimited Talk & Text', 'price': 25.00, 'description': 'Unlimited domestic talk and text'},
            {'name': 'Unlimited Data', 'price': 35.00, 'description': 'Unlimited high-speed data'},
            {'name': 'International Calling', 'price': 15.00, 'description': 'Unlimited international calling'},
            {'name': 'Mobile Hotspot', 'price': 20.00, 'description': '10GB mobile hotspot'},
            {'name': 'Device Protection', 'price': 12.00, 'description': 'Complete device protection plan'},
        ]

        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                name=service_data['name'],
                defaults={
                    'price': service_data['price'],
                    'description': service_data['description']
                }
            )
            if created:
                self.stdout.write(f"Created service: {service.name}")

        # Create sample accounts if none exist
        if Account.objects.count() == 0:
            self.stdout.write("Creating sample accounts...")
            
            # Create 10 sample accounts
            for i in range(1, 11):
                account = Account.objects.create(
                    account_name=f"Account {i:03d}",
                    account_number=f"ACC{i:06d}",
                    status=random.choice(['Active', 'Suspended', 'Pending']),
                    billing_address=f"{random.randint(100, 9999)} Main St, City {i}, ST {i:05d}",
                    monthly_bill=round(random.uniform(50, 300), 2),
                    due_date=datetime.now().date() + timedelta(days=random.randint(1, 30))
                )

                # Create 2-5 lines per account
                num_lines = random.randint(2, 5)
                for j in range(1, num_lines + 1):
                    phone_number = f"({random.randint(200, 999)}) {random.randint(200, 999)}-{random.randint(1000, 9999)}"
                    line = Line.objects.create(
                        account=account,
                        line_name=f"Line {j}",
                        phone_number=phone_number,
                        status=random.choice(['Active', 'Suspended', 'Inactive']),
                        monthly_charge=round(random.uniform(25, 85), 2),
                        device_model=random.choice(['iPhone 15 Pro', 'Samsung Galaxy S24', 'Google Pixel 8', 'iPhone 14', 'Samsung Galaxy A54']),
                        device_color=random.choice(['Black', 'White', 'Blue', 'Red', 'Green', 'Purple']),
                        plan_name=random.choice(['Unlimited Premium', 'Unlimited Plus', 'Unlimited Basic', 'Family Plan', 'Senior Plan']),
                        data_usage_gb=round(random.uniform(5, 50), 1),
                        data_limit_gb=random.choice([25, 50, 100, 999]),  # 999 represents unlimited
                        payment_due_date=datetime.now().date() + timedelta(days=random.randint(1, 30))
                    )

                    # Add 1-3 services per line
                    services = Service.objects.all()
                    selected_services = random.sample(list(services), random.randint(1, min(3, len(services))))
                    for service in selected_services:
                        LineService.objects.create(line=line, service=service)

                self.stdout.write(f"Created account: {account.account_name} with {num_lines} lines")

            self.stdout.write(f"Successfully created {Account.objects.count()} accounts with {Line.objects.count()} total lines")
        else:
            self.stdout.write(f"Database already has {Account.objects.count()} accounts")

        self.stdout.write(self.style.SUCCESS('Production setup completed successfully!'))
        self.stdout.write(f"Login credentials: username='sm', password='sunjava@123'")
