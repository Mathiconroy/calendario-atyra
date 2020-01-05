from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .forms import AddClientForm
from .models import Reservas

import datetime

def index(request): # TODO: Populate the table (Having problems with the logic)
    # reservas = (Reservas.objects.filter(fecha_inicio__lte=datetime.date.today() + datetime.timedelta(days=30)), False)
    reservas = Reservas.objects.filter(fecha_inicio__lte=datetime.date.today() + datetime.timedelta(days=30))
    date_list = [datetime.date.today() + datetime.timedelta(days=x) for x in range(30)]
    """
    if reservas:
        for date in date_list:
            for reserva in reservas:
                if reserva[0].fecha_inicio <= date <= reserva[0].fecha_fin:
                    reserva[1] = True
    """
    return render(request, 'calendarios/main.html', {'reservas':reservas, 'date_list':date_list})

def add_client_form(request):
    if request.method == "POST":
        form = AddClientForm(request.POST)
        if form.is_valid():
            # form = form.clean() # This is here to validate again with my custom clean() method in forms.py
            r = Reservas(casa=form.cleaned_data['casa'], nombre=form.cleaned_data['nombre'], cantidad_personas=form.cleaned_data['cantidad_personas'],
                        fecha_inicio=form.cleaned_data['fecha_inicio'], fecha_fin=form.cleaned_data['fecha_fin'], notas=form.cleaned_data['notas'])
            r.save()
            return redirect('index')

    if request.method == "GET":
        form = AddClientForm()

    return render(request, 'calendarios/form.html', {'form':form})