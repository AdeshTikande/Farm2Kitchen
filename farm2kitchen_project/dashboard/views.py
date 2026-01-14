from django.shortcuts import render
from django.db.models import Sum
from django.db.models.functions import TruncDay, TruncMonth
from django.utils import timezone
from datetime import timedelta
import json
from .models import Order, Profile, Product
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from .forms import AddFarmerForm # Import the form we just made
from django.contrib import messages
import csv
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
# ... existing views ...
from .forms import AddFarmerForm, AddHotelForm # <--- Add AddHotelForm here
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages # To show error messages
def add_farmer(request):
    if request.method == 'POST':
        form = AddFarmerForm(request.POST)
        if form.is_valid():
            # 1. Create the User Account first
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password='password123' # Default password for now
            )
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            # 2. Create the Profile linked to that User
            profile = Profile.objects.create(
                user=user,
                role='farmer', # IMPORTANT: Set role to farmer
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                is_approved=True
            )
            
            messages.success(request, 'New Farmer added successfully!')
            return redirect('manage_farmers')
    else:
        form = AddFarmerForm()

    return render(request, 'dashboard/add_farmer.html', {'form': form})

# ... existing views ...

def delete_user(request, user_id):
    # Get the user or show 404 error
    user = get_object_or_404(User, id=user_id)
    
    # Check role to decide where to redirect after deleting
    # We use a try/except block in case the user has no profile
    try:
        role = user.profile.role
    except:
        role = 'farmer' # Default fallback

    # Delete the user (This deletes Profile, Products, and Orders automatically)
    user.delete()
    
    # Redirect back to the correct page
    if role == 'hotel':
        return redirect('manage_hotels')
    return redirect('manage_farmers')

# --- 1. DASHBOARD ---
def admin_dashboard(request):
    period = request.GET.get('period', 'weekly')
    today = timezone.now()
    
    if period == 'monthly':
        start_date = today - timedelta(days=30)
        trunc_func = TruncDay('order_date')
    elif period == 'yearly':
        start_date = today - timedelta(days=365)
        trunc_func = TruncMonth('order_date')
    else:
        start_date = today - timedelta(days=7)
        trunc_func = TruncDay('order_date')

    orders = Order.objects.filter(status='Completed', order_date__gte=start_date)
    
    chart_data_query = orders.annotate(period=trunc_func).values('period').annotate(total=Sum('total_price')).order_by('period')

    labels = []
    data = []
    for entry in chart_data_query:
        if period == 'yearly':
            labels.append(entry['period'].strftime('%b'))
        else:
            labels.append(entry['period'].strftime('%d %b'))
        data.append(float(entry['total']))

    total_revenue = orders.aggregate(Sum('total_price'))['total_price__sum'] or 0
    platform_earnings = float(total_revenue) * 0.10
    active_farmers = Profile.objects.filter(role__iexact='farmer').count()
    active_hotels = Profile.objects.filter(role__iexact='hotel').count()

    context = {
        'total_revenue': total_revenue,
        'platform_earnings': platform_earnings,
        'active_farmers': active_farmers,
        'active_hotels': active_hotels,
        'chart_labels': json.dumps(labels),
        'chart_data': json.dumps(data),
        'selected_period': period
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

# --- 2. MANAGE PAGES ---
def manage_farmers(request):
    # Use iexact to fix the "capital letter" issue
    farmers = Profile.objects.filter(role__iexact='farmer')
    return render(request, 'dashboard/manage_farmers.html', {'farmers': farmers})

def manage_hotels(request):
    hotels = Profile.objects.filter(role__iexact='hotel')
    return render(request, 'dashboard/manage_hotels.html', {'hotels': hotels})

def manage_products(request):
    products = Product.objects.all()
    return render(request, 'dashboard/manage_products.html', {'products': products})

def add_hotel(request):
    if request.method == 'POST':
        form = AddHotelForm(request.POST)
        if form.is_valid():
            # 1. Create User
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password='password123' 
            )
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            # 2. Create Profile with role='hotel'
            Profile.objects.create(
                user=user,
                role='hotel', # <--- IMPORTANT: This makes them a Hotel
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                is_approved=True
            )
            
            return redirect('manage_hotels')
    else:
        form = AddHotelForm()

    return render(request, 'dashboard/add_hotel.html', {'form': form})


def manage_products(request):
    products = Product.objects.all()
    # We pass 'products' to the HTML file
    return render(request, 'dashboard/manage_products.html', {'products': products})

# Don't forget the delete logic we added earlier!
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('manage_products')


def export_report(request):
    # 1. Get the time period from the URL (default to 'monthly')
    period = request.GET.get('period', 'monthly')

    # 2. Calculate the date range
    today = timezone.now()
    if period == 'weekly':
        start_date = today - timedelta(days=7)
        filename = "report_weekly.csv"
    elif period == 'yearly':
        start_date = today - timedelta(days=365)
        filename = "report_yearly.csv"
    else: # monthly
        start_date = today - timedelta(days=30)
        filename = "report_monthly.csv"

    # 3. Create the CSV Response Object
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # 4. Create the CSV Writer
    writer = csv.writer(response)

    # 5. Write the Header Row
    writer.writerow(['Date Joined', 'Username', 'Role', 'Email', 'Phone', 'Status'])

    # 6. Query the Database (Filter by date joined)
    # Note: We are filtering Profile based on the User's join date
    users = Profile.objects.select_related('user').filter(user__date_joined__gte=start_date)

    # 7. Write the Data Rows
    for profile in users:
        writer.writerow([
            profile.user.date_joined.strftime("%Y-%m-%d %H:%M"), # Date
            profile.user.username,                               # Name
            profile.role.capitalize(),                           # Role (Farmer/Hotel)
            profile.user.email,                                  # Email
            profile.phone,                                       # Phone
            "Active" if profile.is_approved else "Pending"       # Status
        ])

    return response

#register form for farmer and hotel

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 1. Create User
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            # 2. Create Profile
            Profile.objects.create(
                user=user,
                role=form.cleaned_data['role'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                is_approved=True  # Auto-approve for now so you can test easily
            )
            
            messages.success(request, 'Account created! Please login.')
            return redirect('login')
    else:
        form = RegisterForm()
    
    return render(request, 'dashboard/register.html', {'form': form})


#login page
# ... existing code ...

def farmer_dashboard(request):
    return render(request, 'dashboard/farmer_dashboard.html')

def hotel_dashboard(request):
    return render(request, 'dashboard/hotel_dashboard.html')

