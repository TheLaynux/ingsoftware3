from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['categoria', 'nombre', 'precio', 'stock', 'image']
        widgets = {
            'categoria': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Categoría'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Precio'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Stock disponible'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }