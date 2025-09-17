from django import forms
from django.contrib.auth.models import User
from robo_app.models import Account, Line
from decimal import Decimal
from datetime import date, timedelta
import random


class AccountForm(forms.ModelForm):
    """Form for creating new accounts without user information"""
    
    # Account fields
    account_type = forms.ChoiceField(
        choices=[
            ('STANDARD', 'Standard'),
            ('PREMIUM', 'Premium'),
            ('BUSINESS', 'Business'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    status = forms.ChoiceField(
        choices=[
            ('ACTIVE', 'Active'),
            ('INACTIVE', 'Inactive'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # Line fields
    num_lines = forms.IntegerField(
        min_value=1,
        max_value=10,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of lines (1-10)'})
    )
    
    class Meta:
        model = Account
        fields = ['account_type', 'status']
    
    def save(self, commit=True):
        # Create account without user
        account = super().save(commit=False)
        account.user = None  # No user associated
        account.account_number = self.generate_account_number()
        account.last_payment_date = date.today() - timedelta(days=random.randint(1, 30))
        account.payment_due_date = date.today() + timedelta(days=random.randint(1, 30))
        
        if commit:
            account.save()
            
            # Create lines for the account
            self.create_lines_for_account(account, self.cleaned_data['num_lines'])
        
        return account
    
    def generate_account_number(self):
        """Generate a unique account number"""
        import random
        while True:
            account_number = f"ACC{random.randint(100000, 999999)}"
            if not Account.objects.filter(account_number=account_number).exists():
                return account_number
    
    def create_lines_for_account(self, account, num_lines):
        """Create lines for the account"""
        device_models = [
            'iPhone 15 Pro', 'iPhone 15', 'iPhone 14 Pro', 'iPhone 14',
            'Samsung Galaxy S24', 'Samsung Galaxy S23', 'Google Pixel 8',
            'OnePlus 12', 'Motorola Edge 50'
        ]
        
        device_colors = ['Black', 'White', 'Blue', 'Red', 'Purple', 'Green', 'Silver', 'Gold']
        device_storage = ['128GB', '256GB', '512GB', '1TB']
        plan_names = [
            'Magenta MAX', 'Magenta', 'Essentials', 'Business Unlimited',
            'Go5G Plus', 'Go5G', 'Connect', 'Simply Prepaid'
        ]
        
        first_names = ['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis']
        
        for i in range(num_lines):
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
            
            # Create the line
            try:
                Line.objects.create(
                    account=account,
                    line_name=f"Line {i+1}",
                    msdn=msdn,
                    employee_name=employee_name,
                    employee_number=employee_number,
                    status='ACTIVE',
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
            except Exception as e:
                # Skip if MSDN already exists
                continue
