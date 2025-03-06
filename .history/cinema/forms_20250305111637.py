from .models import Reserva, Pelicula
import datetime
from django import forms


class ReservaForm(forms.ModelForm):
    productos = forms.ModelMultipleChoiceField(
        queryset=Pelicula.objects.all(),z
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = Reserva
        fields = ['fecha', 'hora', 'personas', 'productos', 'mensaje']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
            'mensaje': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Mensaje adicional (opcional)'}),
        }
    
    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        hoy = datetime.date.today()
        
        if fecha < hoy:
            raise forms.ValidationError("No puedes hacer reservas en fechas pasadas")
        
        return fecha
    
    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')

        if fecha and hora and not self.instance.pk:
            if Reserva.objects.filter(fecha=fecha, hora=hora).exists():
                raise forms.ValidationError("Ya existe una reserva para esta fecha y hora. Por favor, selecciona otro horario.")
                
        return cleaned_data
    
from .models import Pedido, DetallePedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['nombre', 'correo', 'telefono', 'comprobante']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'id': 'nombre'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'id': 'correo'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'id': 'telefono'}),
            'comprobante': forms.FileInput(attrs={'class': 'form-control', 'id': 'factura'}),
            }    

