from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Reservas

from datetime import timedelta

class AddClientForm(forms.Form): # If let blank, they are REQUIRED by DEFAULT
    id = forms.IntegerField(required=False, label='ID', widget=forms.HiddenInput())
    casa = forms.ChoiceField(label='Casa', choices=[('', 'Seleccione una casa'), (1, 'Barro Roga'), (2, 'Ysypo Roga'), (3, 'Hierro Roga')], widget=forms.Select(attrs={'class':'form-control'}))
    nombre = forms.CharField(label='Nombre', max_length=150, strip=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre del cliente'}))
    email = forms.EmailField(required=False, label='Email', widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email del cliente'}))
    cantidad_personas = forms.IntegerField(label='Cantidad de personas', min_value=1, max_value=10, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Cantidad de personas'}))
    fecha_inicio = forms.DateField(label='Fecha de inicio', widget=forms.DateInput(attrs={'class':'form-control', 'type':'date'}))
    fecha_fin = forms.DateField(label='Fecha de fin', widget=forms.DateInput(attrs={'class':'form-control', 'type':'date'}))
    cantidad_dias = forms.IntegerField(label='Cantidad de dias', min_value=0, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Cantidad de dias'}))
    notas = forms.CharField(required=False, label='Notas', widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Notas'}))
    edit = forms.BooleanField(label='Editar', required=False, widget=forms.HiddenInput())

    # NOTE TO SELF: PYTHON EVALUATES 0 TO FALSE AND OTHER NUMBERS TO TRUE LMAOOOOOOOOOOOO
    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        casa = cleaned_data.get('casa')
        cantidad_dias = cleaned_data.get('cantidad_dias')
        edit = cleaned_data.get('edit')
        id = cleaned_data.get('id')

        if (fecha_fin and fecha_inicio and cantidad_dias) or (fecha_fin and fecha_inicio and cantidad_dias == 0):
            if not ((fecha_fin - fecha_inicio) >= timedelta(days=0)):
                raise forms.ValidationError("ERROR: La fecha final es antes de la fecha inicial.")
            if not ((fecha_fin - fecha_inicio) == timedelta(days=cantidad_dias)):
                raise forms.ValidationError('ERROR: La cantidad de dias introducida no coincide con la fecha inicial y final.')
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
                    raise forms.ValidationError("ERROR: Esta fecha ya fue reservada para esta casa.")
            else: # This is the same check as the last one but it excludes the entry that's being updated (so the edit doesn't clash with it)
                if (Reservas.objects.filter(fecha_inicio__range=(fecha_inicio, fecha_fin)).filter(casa=int(casa)).exclude(id=id) or
                    Reservas.objects.filter(fecha_fin__range=(fecha_inicio, fecha_fin)).filter(casa=int(casa)).exclude(id=id) or 
                    Reservas.objects.filter(fecha_inicio__gte=fecha_inicio).filter(fecha_fin__lte=fecha_fin).filter(casa=int(casa)).exclude(id=id)):
                    raise forms.ValidationError("ERROR: Esta fecha ya fue reservada para esta casa.")

        return cleaned_data

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Usuario', strip=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre de usuario'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class':'form-control'}))