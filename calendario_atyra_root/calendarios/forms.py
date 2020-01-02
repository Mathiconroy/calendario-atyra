from django import forms

class AddClientForm(forms.Form): # If let blank, they are REQUIRED by default
    # TODO: Add a validator for fecha_inicio and fecha_fin (There MUST NOT be a reservation in that house between the two dates!!!)
    casa = forms.ChoiceField(label='Casa', choices=[('', 'Seleccione una casa'), ('1', '1'), ('2', '2'), ('3', '3')], widget=forms.Select(attrs={'class':'form-control'}))
    nombre = forms.CharField(label='Nombre', max_length=150, strip=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre del cliente'}))
    cantidad_personas = forms.IntegerField(label='Cantidad de personas', min_value=1, max_value=10, widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Cantidad de personas'}))
    fecha_inicio = forms.DateField(label='Fecha de inicio', widget=forms.DateInput(attrs={'class':'form-control', 'type':'date'}))
    fecha_fin = forms.DateField(label='Fecha de fin', widget=forms.DateInput(attrs={'class':'form-control', 'type':'date'}))
    notas = forms.CharField(label='Notas', widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Notas'}))