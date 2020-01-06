from django import forms
from .models import Reservas

from datetime import timedelta

def validate_date(value):
    pass

class AddClientForm(forms.Form): # If let blank, they are REQUIRED by default
    # TODO: Add a validator for fecha_inicio and fecha_fin (There MUST NOT be a reservation in that house between the two dates!!!)
    casa = forms.ChoiceField(label='Casa', choices=[('', 'Seleccione una casa'), ('1', 'Barro Roga'), ('2', 'Ysypo Roga'), ('3', 'Hierro Roga')], widget=forms.Select(attrs={'class':'form-control'}))
    nombre = forms.CharField(label='Nombre', max_length=150, strip=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre del cliente'}))
    cantidad_personas = forms.IntegerField(label='Cantidad de personas', min_value=1, max_value=10, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Cantidad de personas'}))
    fecha_inicio = forms.DateField(label='Fecha de inicio', widget=forms.DateInput(attrs={'class':'form-control', 'type':'date'}))
    fecha_fin = forms.DateField(label='Fecha de fin', widget=forms.DateInput(attrs={'class':'form-control', 'type':'date'}))
    # Add email field?
    notas = forms.CharField(required=False, label='Notas', widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Notas'}))
    warning = forms.BooleanField(required=False)

    def clean(self): # TODO: ADD A WARNING IF A RESERVATION IS MORE THAN X DAYS LONG, MOM SCARED THE SHIT OUT OF ME
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        casa = cleaned_data.get('casa')
        warning = cleaned_data.get('warning')

        if fecha_fin and fecha_inicio:
            if not ((fecha_fin - fecha_inicio) >= timedelta(days=0)):
                raise forms.ValidationError("ERROR: La fecha final es antes de la fecha inicial.")
            if Reservas.objects.filter(fecha_inicio__gte=fecha_inicio).filter(fecha_fin__lte=fecha_fin).filter(casa=casa):
                raise forms.ValidationError("ERROR: Esta fecha ya fue reservada para esta casa.")
            if ((fecha_fin - fecha_inicio) >= timedelta(days=7)):
                warning = False
                self.add_error('fecha_fin', 'ADVERTENCIA: La reserva dura más de 7 dias. Checke la caja al final del formulario para confirmar los datos ingresados.')

        return cleaned_data
    