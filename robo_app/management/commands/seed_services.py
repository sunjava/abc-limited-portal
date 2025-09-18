from django.core.management.base import BaseCommand
from robo_app.models import Service


class Command(BaseCommand):
    help = 'Seed services in the database'

    def handle(self, *args, **options):
        self.stdout.write('Seeding services...')
        
        # Check if services already exist
        if Service.objects.exists():
            self.stdout.write('Services already exist. Skipping seeding.')
            return
        
        # Create services
        services_data = [
            {
                'name': '1 Day International Pass',
                'service_type': 'INTERNATIONAL_PASS',
                'description': 'Perfect for short trips. 24-hour high-speed data with unlimited calling and texting.',
                'price': 1.00,
                'duration_days': 1,
                'data_allowance_mb': 512,
                'features': ['Unlimited calling', 'Unlimited texting', '512MB high-speed data']
            },
            {
                'name': 'International Calling',
                'service_type': 'CALLING_ADDON',
                'description': 'Add international calling to your existing plan.',
                'price': 15.00,
                'duration_days': 30,
                'data_allowance_mb': None,
                'features': ['International calling to 200+ countries', 'No roaming charges']
            },
            {
                'name': '5GB Data Add-On',
                'service_type': 'DATA_ADDON',
                'description': 'Additional 5GB of high-speed data for your current billing cycle.',
                'price': 25.00,
                'duration_days': 30,
                'data_allowance_mb': 5120,
                'features': ['5GB additional data', 'High-speed 4G/5G', 'No overage charges']
            },
            {
                'name': 'International Pass - Europe',
                'service_type': 'INTERNATIONAL_PASS',
                'description': '7-day pass for travel to Europe with unlimited data and calling.',
                'price': 25.00,
                'duration_days': 7,
                'data_allowance_mb': 2048,
                'features': ['Unlimited calling', 'Unlimited texting', '2GB high-speed data', 'Europe coverage']
            },
            {
                'name': '10 Day International Pass',
                'service_type': 'INTERNATIONAL_PASS',
                'description': '10-day international pass with 5GB data and unlimited calling.',
                'price': 35.00,
                'duration_days': 10,
                'data_allowance_mb': 5120,
                'features': ['Unlimited calling', 'Unlimited texting', '5GB high-speed data', 'Global coverage']
            },
            {
                'name': 'Data Add-on - 10GB',
                'service_type': 'DATA_ADDON',
                'description': 'Additional 10GB of high-speed data for heavy users.',
                'price': 35.00,
                'duration_days': 30,
                'data_allowance_mb': 10240,
                'features': ['10GB additional data', 'High-speed 4G/5G', 'No overage charges', 'Priority data']
            },
            {
                'name': '30 Day International Pass',
                'service_type': 'INTERNATIONAL_PASS',
                'description': '30-day international pass with 15GB data and unlimited calling.',
                'price': 50.00,
                'duration_days': 30,
                'data_allowance_mb': 15360,
                'features': ['Unlimited calling', 'Unlimited texting', '15GB high-speed data', 'Global coverage', 'Premium support']
            }
        ]
        
        created_count = 0
        for service_data in services_data:
            try:
                Service.objects.create(
                    name=service_data['name'],
                    service_type=service_data['service_type'],
                    description=service_data['description'],
                    price=service_data['price'],
                    duration_days=service_data['duration_days'],
                    data_allowance_mb=service_data['data_allowance_mb'],
                    features=service_data['features'],
                    is_active=True
                )
                created_count += 1
                self.stdout.write(f'Created service: {service_data["name"]}')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to create service {service_data["name"]}: {e}'))
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} services'))
