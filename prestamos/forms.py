from django import forms
from .models import Prestamo

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['tipo_prestamo', 'fecha_inicio', 'monto']

    def clean(self):
        cleaned_data = super().clean()
        cliente = self.initial['cliente']
        monto = cleaned_data.get('monto')
        tipo_cliente = cliente.tipo

        limites = {
            'BLACK': 500000,
            'GOLD': 300000,
            'CLASSIC': 100000,
        }
        
        if monto > limites[tipo_cliente]:
            raise forms.ValidationError(f"El monto máximo permitido para {tipo_cliente} es {limites[tipo_cliente]}")
        return cleaned_data
