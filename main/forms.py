from django import forms
from .models import *


class addProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'discount_price', 'image1', 'image2', 'image3', 'still_instock']

class updateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'discount_price', 'image1', 'image2', 'image3', 'still_instock']


class addCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class messageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'phone_number', 'message']
