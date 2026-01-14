from django.urls import path

from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('farmers/', views.manage_farmers, name='manage_farmers'),  # <--- CHECK THIS LINE
    path('hotels/', views.manage_hotels, name='manage_hotels'),
    path('products/', views.manage_products, name='manage_products'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('add-farmer/', views.add_farmer, name='add_farmer'),
    path('add-hotel/', views.add_hotel, name='add_hotel'),
 
    path('products/', views.manage_products, name='manage_products'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('export-report/', views.export_report, name='export_report'),


    # ... other paths ...
    path('farmer/', views.farmer_dashboard, name='farmer_dashboard'),
    path('hotel/', views.hotel_dashboard, name='hotel_dashboard'),


]
