from django import forms
from .models import Product, Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# ---------------- Product Form ----------------
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'اسم المنتج', 'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'placeholder': 'السعر', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'وصف المنتج', 'class': 'form-control', 'rows': 3}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

# ---------------- Order Form ----------------
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'phone', 'address']
        widgets = {
            'customer_name': forms.TextInput(attrs={'placeholder': 'الاسم الكامل', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': 'رقم الهاتف', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'placeholder': 'عنوان التوصيل', 'class': 'form-control', 'rows': 3}),
        }

# ---------------- Customer Registration Form ----------------
class CustomerRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'اسم المستخدم', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'البريد الإلكتروني', 'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'كلمة المرور', 'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'تأكيد كلمة المرور', 'class': 'form-control'}),
        }
