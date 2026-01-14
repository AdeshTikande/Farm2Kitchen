from django.db import models
from django.contrib.auth.models import User

# 1. EXTENDED USER PROFILE (For Farmer vs Hotel distinction)
class Profile(models.Model):
    ROLE_CHOICES = (('farmer', 'Farmer'), ('hotel', 'Hotel'), ('admin', 'Admin'))
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False) # Admin must approve them

    def __str__(self):
        return f"{self.user.username} ({self.role})"

# 2. PRODUCT MODEL (What farmers sell)
class Product(models.Model):
    CATEGORY_CHOICES = (('Veg', 'Vegetables'), ('Fruit', 'Fruits'), ('Grain', 'Grains'), ('Dairy', 'Dairy'))
    
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.FloatField() # in kg
    is_active = models.BooleanField(default=True) # Admin can hide product

    def __str__(self):
        return f"{self.name} - ₹{self.price_per_kg}/kg"

# 3. ORDER MODEL (Transactions)
class Order(models.Model):
    STATUS_CHOICES = (('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled'))

    hotel = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Order #{self.id} by {self.hotel.username}"