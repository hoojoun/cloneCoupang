from django import forms
from .models import Products


class ProductRegisterForm(forms.Form):
    class Meta:
        model = Products
        fields = ['name', 'price', 'seller', 'image', ]
