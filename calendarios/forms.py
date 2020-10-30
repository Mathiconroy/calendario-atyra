from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Reservas

from datetime import timedelta

precio_adultos = 150000
precio_menores = 120000

class AddClientForm(forms.Form): # REQUIRED is True by DEFAULT
    # TODO: Ask mom if two people can REQUEST a reservation on the same date
    id = forms.IntegerField(required=False, label='ID', widget=forms.HiddenInput())
    casa = forms.ChoiceField(label='Casa', choices=[('', 'Seleccione una casa'), (1, 'Barro Roga'), (2, 'Ysypo Roga'), (3, 'Hierro Roga')], widget=forms.Select(attrs={'class':'form-control'}))
    nombre = forms.CharField(label='Nombre', max_length=150, strip=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre del cliente'}))
    email = forms.EmailField(required=False, label='Email', widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email del cliente'}))
    cantidad_adultos = forms.IntegerField(label='Cantidad de adultos (a partir de 13 años)', initial=0, min_value=1, max_value=10, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Cantidad de adultos'}))
    cantidad_menores = forms.IntegerField(label='Cantidad de niños (entre 2 a 12 años)', initial=0, min_value=0, max_value=10, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Cantidad de niños'}))
    cantidad_gratis = forms.IntegerField(label='Cantidad de menores de 23 meses', initial=0, min_value=0, max_value=10, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Cantidad de menores de 18 meses'}))
    fecha_inicio = forms.DateField(label='Fecha de inicio', widget=forms.DateInput(attrs={'class':'form-control', 'type':'date'}))
    fecha_fin = forms.DateField(label='Fecha de fin', widget=forms.DateInput(attrs={'class':'form-control', 'type':'date'}))
    tipo_adelanto = forms.ChoiceField(label='Medio de seña', choices=[('', 'Seleccione un metodo'), (1, 'Giro'), (2, 'Depósito bancario')], widget=forms.Select(attrs={'class':'form-control'}))
    notas = forms.CharField(required=False, label='Notas', widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Notas', 'size':1}))
    edit = forms.BooleanField(label='Editar', required=False, widget=forms.HiddenInput())
    confirm = forms.BooleanField(label='Confirm', required=False, widget=forms.HiddenInput())

    # NOTE TO SELF: PYTHON EVALUATES 0 TO FALSE AND OTHER NUMBERS TO TRUE LMAOOOOOOOOOOOO
    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        casa = cleaned_data.get('casa')
        edit = cleaned_data.get('edit')
        id = cleaned_data.get('id')
        cantidad_adultos = cleaned_data.get('cantidad_adultos')
        cantidad_menores = cleaned_data.get('cantidad_menores')

        if fecha_fin and fecha_inicio:
            if not ((fecha_fin - fecha_inicio) >= timedelta(days=0)):
                raise forms.ValidationError("ERROR: La fecha final es antes de la fecha inicial.")
            if casa == '':
                self.add_error('casa', 'ERROR: La casa seleccionada no es válida.')
            if not edit: 
                # Check if fecha_fin and fecha_inicio are between a:
                # fecha_inicio of a row
                # fecha_fin of a row
                # fecha_inicio and fecha_fin of a row
                if (Reservas.objects.filter(fecha_inicio__range=(fecha_inicio, fecha_fin)).filter(casa=int(casa)) or
                    Reservas.objects.filter(fecha_fin__range=(fecha_inicio, fecha_fin)).filter(casa=int(casa)) or 
                    Reservas.objects.filter(fecha_inicio__gte=fecha_inicio).filter(fecha_fin__lte=fecha_fin).filter(casa=int(casa))):
                    raise forms.ValidationError("ERROR: El rango de fechas seleccionado no está disponible para esta casa.")
            else: # This is the same check as the last one but it excludes the entry that's being updated (so the edit doesn't clash with it)
                if (Reservas.objects.filter(fecha_inicio__range=(fecha_inicio, fecha_fin)).filter(casa=int(casa)).exclude(id=id) or
                    Reservas.objects.filter(fecha_fin__range=(fecha_inicio, fecha_fin)).filter(casa=int(casa)).exclude(id=id) or 
                    Reservas.objects.filter(fecha_inicio__gte=fecha_inicio).filter(fecha_fin__lte=fecha_fin).filter(casa=int(casa)).exclude(id=id)):
                    raise forms.ValidationError("ERROR: El rango de fechas seleccionado no está disponible para esta casa.")
        
        # TODO: Confirm with mom whether cantidad_gratis should count for the total or not, I'm leaving it without it for the time being.
        if cantidad_adultos + cantidad_menores <= 0 or cantidad_adultos + cantidad_menores > 10:
            raise forms.ValidationError('ERROR: La cantidad de personas es invalida.')

        return cleaned_data

class ChangePaymentForm(forms.Form):
    cantidad_deposito = forms.IntegerField(label='Cantidad', min_value=0, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Cantidad'}))
    # TODO: Validate this, the difference can't be negative lmao

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Usuario', strip=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre de usuario'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class':'form-control'}))