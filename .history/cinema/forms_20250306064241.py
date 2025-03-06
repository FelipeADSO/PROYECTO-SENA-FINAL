from .models import Reserva, Pelicula
import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class FormularioRegistroUsuario(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class ReservaForm(forms.ModelForm):
    productos = forms.ModelMultipleChoiceField(
        queryset=Pelicula.objects.all(),
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
<<<<<<< HEAD
    
=======
    

from .models import Orden

class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ['nombre', 'email', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tucorreo@ejemplo.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu número de teléfono'})
        }
>>>>>>> 0d8c1276fdc6450568f12d66070e856160c4d5a8
