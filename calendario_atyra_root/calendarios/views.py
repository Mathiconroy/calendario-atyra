from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .forms import AddClientForm
from .models import Reservas

from datetime import date, datetime, timedelta

def index(request): # TODO: Populate the table (Having problems with the logic)
    reserva = Reservas.objects.filter(fecha_inicio__lte=date.today() + timedelta(days=30))
    return render(request, 'calendarios/main.html', {'reservas':reserva})

def add_client_form(request):
    if request.method == "POST":
        form = AddClientForm(request.POST)
        if form.is_valid():
            form = form.clean() # This is here to validate again with my custom clean() method in forms.py
            r = Reservas(casa=form.cleaned_data['casa'], nombre=form.cleaned_data['nombre'], cantidad_personas=form.cleaned_data['cantidad_personas'],
                        fecha_inicio=form.cleaned_data['fecha_inicio'], fecha_fin=form.cleaned_data['fecha_fin'], notas=form.cleaned_data['notas'])
            r.save()
            return render(request, 'calendarios/main.html')

    if request.method == "GET":
        form = AddClientForm()

    return render(request, 'calendarios/form.html', {'form':form})