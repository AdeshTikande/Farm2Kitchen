from django.contrib import admin
from .models import Profile, Product, Order

# This makes the models visible in the Admin Panel
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone', 'is_approved')
    list_filter = ('role', 'is_approved')
    search_fields = ('user__username', 'phone')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'farmer', 'category', 'price_per_kg', 'is_active')
    list_filter = ('category', 'is_active')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'hotel', 'product', 'total_price', 'status', 'order_date')
    list_filter = ('status', 'order_date')