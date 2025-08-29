from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date, timedelta
import random
from robo_app.models import Account, Line, Service, LineService


class Command(BaseCommand):
    help = 'Populate the database with 100 accounts and their lines'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating 100 accounts with lines...'))
        
        # Create a test user if it doesn't exist
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(f'Created user: {user.username}')

        # Account types and statuses for variety
        account_types = ['STANDARD', 'PREMIUM', 'BUSINESS']
        account_statuses = ['ACTIVE', 'INACTIVE']
        line_statuses = ['ACTIVE', 'SUSPENDED', 'CANCELLED']
        
        # Device models for variety
        device_models = [
            'iPhone 15 Pro', 'iPhone 15', 'iPhone 14 Pro', 'iPhone 14',
            'Samsung Galaxy S24', 'Samsung Galaxy S23', 'Google Pixel 8',
            'OnePlus 12', 'Motorola Edge 50'
        ]
        
        device_colors = ['Black', 'White', 'Blue', 'Red', 'Purple', 'Green', 'Silver', 'Gold']
        device_storage = ['128GB', '256GB', '512GB', '1TB']
        
        # Plan names
        plan_names = [
            'Magenta MAX', 'Magenta', 'Essentials', 'Business Unlimited',
            'Go5G Plus', 'Go5G', 'Connect', 'Simply Prepaid'
        ]
        
        # Employee names for variety
        first_names = [
            'James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda',
            'William', 'Elizabeth', 'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica',
            'Thomas', 'Sarah', 'Christopher', 'Karen', 'Charles', 'Nancy', 'Daniel', 'Lisa',
            'Matthew', 'Betty', 'Anthony', 'Helen', 'Mark', 'Sandra', 'Donald', 'Donna',
            'Steven', 'Carol', 'Paul', 'Ruth', 'Andrew', 'Sharon', 'Joshua', 'Michelle',
            'Kenneth', 'Laura', 'Kevin', 'Sarah', 'Brian', 'Kimberly', 'George', 'Deborah',
            'Timothy', 'Dorothy', 'Ronald', 'Lisa', 'Jason', 'Nancy', 'Edward', 'Karen'
        ]
        
        last_names = [
            'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
            'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
            'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson',
            'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker',
            'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill',
            'Flores', 'Green', 'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell'
        ]

        accounts_created = 0
        lines_created = 0

        for i in range(100):
            # Generate account number
            account_number = f"ACC{str(i+1).zfill(6)}"  # ACC000001, ACC000002, etc.
            
            # Create account
            account, created = Account.objects.get_or_create(
                account_number=account_number,
                defaults={
                    'user': user,
                    'status': random.choice(account_statuses),
                    'account_type': random.choice(account_types),
                    'last_payment_date': date.today() - timedelta(days=random.randint(1, 60)),
                    'payment_due_date': date.today() + timedelta(days=random.randint(1, 30))
                }
            )
            
            if created:
                accounts_created += 1
                self.stdout.write(f'Created account: {account.account_number}')
                
                # Create 1-15 lines per account
                num_lines = random.randint(1, 15)
                
                for j in range(num_lines):
                    # Generate unique MSDN
                    area_code = random.choice(['555', '212', '310', '415', '713', '404', '305'])
                    phone_number = f"{random.randint(1000000, 9999999)}"
                    msdn = f"+1-{area_code}-{phone_number[:3]}-{phone_number[3:]}"
                    
                    # Generate employee details
                    first_name = random.choice(first_names)
                    last_name = random.choice(last_names)
                    employee_name = f"{first_name} {last_name}"
                    employee_number = f"EMP{random.randint(1000, 9999)}"
                    
                    # Generate device details
                    device_model = random.choice(device_models)
                    device_color = random.choice(device_colors)
                    storage = random.choice(device_storage)
                    device_price = Decimal(str(random.randint(200, 1200)))
                    
                    # Generate plan details
                    plan_name = random.choice(plan_names)
                    plan_price = Decimal(str(random.randint(30, 120)))
                    
                    # Protection details
                    protection_options = [
                        ('Protection<360>', Decimal('18.00')),
                        ('Basic Protection', Decimal('7.00')),
                        ('Premium Protection', Decimal('15.00')),
                        ('No Protection', Decimal('0.00'))
                    ]
                    protection_name, protection_price = random.choice(protection_options)
                    
                    # Calculate payment due date
                    payment_due_date = date.today() + timedelta(days=random.randint(5, 30))
                    
                    # Determine line status (most should be active)
                    if account.status == 'INACTIVE':
                        line_status = 'CANCELLED'  # Inactive accounts have cancelled lines
                    else:
                        # 70% active, 20% suspended, 10% cancelled
                        rand = random.random()
                        if rand < 0.7:
                            line_status = 'ACTIVE'
                        elif rand < 0.9:
                            line_status = 'SUSPENDED'
                        else:
                            line_status = 'CANCELLED'
                    
                    # Try to create the line, skip if MSDN already exists
                    try:
                        line = Line.objects.create(
                            account=account,
                            line_name=f"Line {j+1}",
                            msdn=msdn,
                            employee_name=employee_name,
                            employee_number=employee_number,
                            status=line_status,
                            payment_due_date=payment_due_date,
                            device_model=device_model,
                            device_color=device_color,
                            device_storage=storage,
                            device_price=device_price,
                            plan_name=plan_name,
                            plan_price=plan_price,
                            plan_data_limit='Unlimited',
                            protection_name=protection_name,
                            protection_price=protection_price,
                            trade_in_value=Decimal(str(random.randint(0, 300))),
                            total_monthly_cost=plan_price + protection_price
                        )
                        lines_created += 1
                    except Exception as e:
                        # Skip if MSDN already exists and generate a new one
                        continue

            else:
                self.stdout.write(f'Account already exists: {account.account_number}')

        # Create services if they don't exist
        services_data = [
            {
                'name': '1 Day International Pass',
                'service_type': 'INTERNATIONAL_PASS',
                'description': 'Perfect for short trips. 24-hour high-speed data with unlimited calling and texting.',
                'price': Decimal('1.00'),
                'duration_days': 1,
                'data_allowance_mb': 512,
                'features': [
                    'Valid for 24 hours from activation',
                    '512MB high-speed data allowance',
                    'Unlimited texting to 210+ countries',
                    'Unlimited calling to 210+ countries',
                    'Works in 210+ countries and destinations',
                    'No overage charges - data stops when limit reached'
                ]
            },
            {
                'name': '10 Day International Pass',
                'service_type': 'INTERNATIONAL_PASS',
                'description': 'Great for business trips and week-long vacations. 10 days of high-speed data with unlimited calling and texting.',
                'price': Decimal('35.00'),
                'duration_days': 10,
                'data_allowance_mb': 5120,  # 5GB
                'features': [
                    'Valid for 10 consecutive days from activation',
                    '5GB high-speed data allowance',
                    'Unlimited texting to 210+ countries',
                    'Unlimited calling to 210+ countries',
                    'Works in 210+ countries and destinations',
                    'No overage charges - data stops when limit reached',
                    'Ideal for week-long business trips or vacations'
                ]
            },
            {
                'name': '30 Day International Pass',
                'service_type': 'INTERNATIONAL_PASS',
                'description': 'Best value for extended travel. 30 days of high-speed data with unlimited calling and texting.',
                'price': Decimal('50.00'),
                'duration_days': 30,
                'data_allowance_mb': 15360,  # 15GB
                'features': [
                    'Valid for 30 consecutive days from activation',
                    '15GB high-speed data allowance',
                    'Unlimited texting to 210+ countries',
                    'Unlimited calling to 210+ countries',
                    'Works in 210+ countries and destinations',
                    'No overage charges - data stops when limit reached',
                    'Perfect for extended international travel',
                    'Best value for frequent international travelers'
                ]
            },
            {
                'name': '5GB Data Add-On',
                'service_type': 'DATA_ADDON',
                'description': 'Additional high-speed data for heavy users.',
                'price': Decimal('25.00'),
                'duration_days': 30,
                'data_allowance_mb': 5120,
                'features': [
                    '5GB additional high-speed data',
                    'Valid for 30 days',
                    'Perfect for streaming and downloads'
                ]
            }
        ]

        services_created = 0
        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                name=service_data['name'],
                defaults=service_data
            )
            if created:
                services_created += 1
                self.stdout.write(f'Created service: {service.name}')

        # Final statistics
        total_accounts = Account.objects.count()
        total_lines = Line.objects.count()
        active_lines = Line.objects.filter(status='ACTIVE').count()
        suspended_lines = Line.objects.filter(status='SUSPENDED').count()
        cancelled_lines = Line.objects.filter(status='CANCELLED').count()
        active_accounts = Account.objects.filter(status='ACTIVE').count()
        inactive_accounts = Account.objects.filter(status='INACTIVE').count()

        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('DATABASE POPULATION COMPLETED!'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(self.style.SUCCESS(f'Accounts created this run: {accounts_created}'))
        self.stdout.write(self.style.SUCCESS(f'Lines created this run: {lines_created}'))
        self.stdout.write(self.style.SUCCESS(f'Services created this run: {services_created}'))
        self.stdout.write(self.style.SUCCESS('\nFINAL DATABASE STATISTICS:'))
        self.stdout.write(self.style.SUCCESS(f'Total Accounts: {total_accounts}'))
        self.stdout.write(self.style.SUCCESS(f'  - Active: {active_accounts}'))
        self.stdout.write(self.style.SUCCESS(f'  - Inactive: {inactive_accounts}'))
        self.stdout.write(self.style.SUCCESS(f'Total Lines: {total_lines}'))
        self.stdout.write(self.style.SUCCESS(f'  - Active: {active_lines}'))
        self.stdout.write(self.style.SUCCESS(f'  - Suspended: {suspended_lines}'))
        self.stdout.write(self.style.SUCCESS(f'  - Cancelled: {cancelled_lines}'))
        self.stdout.write(self.style.SUCCESS('\nYour dashboard will now show rich data!'))
        self.stdout.write(self.style.SUCCESS('Visit: http://localhost:8000/dashboard/'))
        self.stdout.write(self.style.SUCCESS(f'Login: username=testuser, password=testpass123'))
