import os
import django
import random
from datetime import timedelta
from django.utils import timezone
from faker import Faker

# 1. SETUP DJANGO ENVIRONMENT
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farm2kitchen_project.settings')
django.setup()

from django.contrib.auth.models import User
from dashboard.models import Profile, Product, Order

fake = Faker('en_IN') # Use Indian names/addresses

def create_data():
    print("🌱 Seeding data... This might take 10 seconds.")
    
    # CLEAR OLD DATA (Optional - uncomment if you want a fresh start)
    # Order.objects.all().delete()
    # Product.objects.all().delete()
    # Profile.objects.all().delete()
    # User.objects.exclude(is_superuser=True).delete()

    # 2. CREATE FARMERS
    farmers = []
    for _ in range(10):
        username = fake.user_name()
        # Ensure unique username
        while User.objects.filter(username=username).exists():
            username = username + str(random.randint(1, 99))
            
        user = User.objects.create_user(username=username, email=fake.email(), password='password123')
        user.first_name = fake.first_name()
        user.last_name = fake.last_name()
        user.save()
        
        Profile.objects.create(user=user, role='farmer', phone=fake.phone_number(), address=fake.address(), is_approved=True)
        farmers.append(user)
        print(f"   - Created Farmer: {user.username}")

    # 3. CREATE HOTELS
    hotels = []
    for _ in range(5):
        username = fake.user_name()
        while User.objects.filter(username=username).exists():
            username = username + str(random.randint(1, 99))

        user = User.objects.create_user(username=username, email=fake.email(), password='password123')
        Profile.objects.create(user=user, role='hotel', phone=fake.phone_number(), address=fake.address(), is_approved=True)
        hotels.append(user)
        print(f"   - Created Hotel: {user.username}")

    # 4. CREATE PRODUCTS
    categories = ['Veg', 'Fruit', 'Grain', 'Dairy']
    products = []
    for farmer in farmers:
        for _ in range(random.randint(2, 5)): # Each farmer has 2-5 products
            prod = Product.objects.create(
                farmer=farmer,
                name=f"{fake.color_name()} {random.choice(['Potato', 'Tomato', 'Onion', 'Rice', 'Milk', 'Apple'])}",
                category=random.choice(categories),
                price_per_kg=random.randint(20, 200),
                quantity_available=random.randint(100, 1000),
                is_active=True
            )
            products.append(prod)
    print(f"   - Created {len(products)} Products")

    # 5. CREATE ORDERS (Spread over last year)
    for _ in range(100): # 100 random transactions
        prod = random.choice(products)
        qty = random.randint(10, 50)
        
        # Random date within last 365 days
        days_ago = random.randint(0, 365)
        order_date = timezone.now() - timedelta(days=days_ago)
        
        order = Order.objects.create(
            hotel=random.choice(hotels),
            product=prod,
            quantity=qty,
            total_price=prod.price_per_kg * qty,
            status='Completed' # Ensure they show up in revenue
        )
        # Hack to override auto_now_add for historical data
        order.order_date = order_date
        order.save()

    print("✅ Data Seeding Completed Successfully!")

if __name__ == '__main__':
    create_data()