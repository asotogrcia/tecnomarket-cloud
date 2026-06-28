from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'descripcion', 'stock', 'imagen_url']
        #Se añade clases de bootstrap a los inputs para que se vean mejor en el front-end
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'imagen_url': forms.URLInput(attrs={'class': 'form-control'}),
        }
