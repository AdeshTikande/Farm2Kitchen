from django import forms
from django.contrib.auth.models import User
from .models import Profile

class AddFarmerForm(forms.ModelForm):
    # Extra fields not in the main User model
    phone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full Address'}))
    
    # Fields from the User model (First Name, Last Name, Email)
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username (for login)'}))

    class Meta:
        model = Profile
        fields = ['phone', 'address'] # We handle User fields manually in the view

        # ... existing imports and AddFarmerForm ...

class AddHotelForm(forms.ModelForm):
    # Same fields as Farmer, just tailored for Hotels
    phone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Hotel Address'}))
    
    first_name = forms.CharField(required=True, label="Hotel Name / Manager Name", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Blue Moon Hotel'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Manager Surname'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Official Email'}))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Login Username'}))

    class Meta:
        model = Profile
        fields = ['phone', 'address']


        # ... existing imports and AddFarmerForm ...

class AddHotelForm(forms.ModelForm):
    # Same fields as Farmer, just tailored for Hotels
    phone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Hotel Address'}))
    
    first_name = forms.CharField(required=True, label="Hotel Name / Manager Name", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Blue Moon Hotel'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Manager Surname'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Official Email'}))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Login Username'}))

    class Meta:
        model = Profile
        fields = ['phone', 'address']
      
      
      
      
      
      
        #RegisterForm for farmer

class RegisterForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Address'}))
    
    # Dropdown to choose Role
    ROLE_CHOICES = [('farmer', 'Farmer'), ('hotel', 'Hotel')]
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))