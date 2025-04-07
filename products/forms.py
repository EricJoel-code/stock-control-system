from django import forms
from .models import Product, ProductModel, Model
from django.core.validators import MinValueValidator


class ProductForm(forms.ModelForm):
    
    models = forms.ModelMultipleChoiceField(
        queryset=Model.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Modelos"
    )
    
    
    class Meta:
        model = Product
        fields = ['description', 'image', 'stock', 'price', 'gender', 'size', 'is_active']
        labels = {
            'description': 'Descripción',
            'image': 'Imagen',
            'stock': 'Cantidad en inventario',
            'price': 'Precio',
            'gender': 'Género',
            'size': 'Talla',
            'is_active': '¿Activar o Desactivar?',
        }
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,  # Ajuste de altura
                'placeholder': 'Describe el producto',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'placeholder': 'Cantidad en inventario',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',  # Permite precios decimales
                'placeholder': 'Precio en dólares',
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control',
            }),
            'size': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Talla del calcetín',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'role': 'switch',
            }),
        }
        
        
class ModelForm(forms.ModelForm):
    class Meta:
        model = Model
        fields = ['description', 'color']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del modelo',
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Color del modelo',
            }),
        }

