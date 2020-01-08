from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.core.mail import send_mail
from .forms import AddClientForm
from .models import Reservas

from datetime import date, timedelta

class TableRow(): # Represents a row in the table in index route
    def __init__(self, dia):
        self.dia = dia
        
    reservas_row = list() # List of all the reservas in that row

def index(request): # TODO: Rewrite this mess, it's a disaster
    # DON'T FORGET THAT CASA IS SAVED AS A STRING IN CASE ITS NAME IS CHANGED!!!!!!!!!!!!
    reservas = Reservas.objects.filter(fecha_inicio__lte=date.today() + timedelta(days=30)).exclude(fecha_fin__lt=date.today()).order_by('fecha_inicio')
    date_list = [date.today() + timedelta(days=x) for x in range(30)]
    reservas_list = []
    # for fecha in date_list: # TODO: See what the actual fuck to do here, it seems impossible
    #    for reserva in reservas:
    return render(request, 'calendarios/main.html', {'fechas':date_list, 'reservas':reservas})

def add_client_form(request):
    if request.method == "POST":
        form = AddClientForm(request.POST)
        if form.is_valid():
            form = form.clean() # This is here to validate again with my custom clean() method in forms.py
            r = Reservas(casa=form['casa'], nombre=form['nombre'], cantidad_personas=form['cantidad_personas'],
                        fecha_inicio=form['fecha_inicio'], fecha_fin=form['fecha_fin'], notas=form['notas'])
            r.save()
            return redirect('index')

    if request.method == "GET":
        form = AddClientForm()

    return render(request, 'calendarios/form.html', {'form':form})

def view_client_form(request, id):
    reserva = Reservas.objects.get(id=id)
    return render(request, 'calendarios/view_form.html', {'reserva':reserva})

def test_mail(request):
    send_mail('Test', 'Hello, this is a test.', 'mathias.martinez018@gmail.com', recipient_list=['mathiconroy@gmail.com'])
    return render(request, 'calendarios/test.html')