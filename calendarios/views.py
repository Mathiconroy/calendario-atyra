from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .forms import AddClientForm
from .models import Reservas

import datetime

class Reserva():
    def __init__(self, dia):
        self.dia = dia

    casa1 = False
    casa2 = False
    casa3 = False

def index(request): # TODO: Populate the table (Having problems with the logic)
    # DON'T FORGET THAT CASA IS SAVED AS A STRING IN CASE ITS NAME IS CHANGED!!!!!!!!!!!!
    reservas = Reservas.objects.filter(fecha_inicio__lte=datetime.date.today() + datetime.timedelta(days=30))
    date_list = [datetime.date.today() + datetime.timedelta(days=x) for x in range(30)]
    reservas_list = []
    for fecha in date_list:
        r = Reserva(dia=fecha)
        for reserva in reservas:
            if reserva.fecha_inicio <= fecha <= reserva.fecha_fin and reserva.casa == "1":
                r.casa1 = True
            elif reserva.fecha_inicio <= fecha <= reserva.fecha_fin and reserva.casa == "2":
                r.casa2 = True
            elif reserva.fecha_inicio <= fecha <= reserva.fecha_fin and reserva.casa == "3":
                r.casa3 = True
        reservas_list.append(r)

    return render(request, 'calendarios/main.html', {'reservas':reservas_list, 'date_list':date_list})

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