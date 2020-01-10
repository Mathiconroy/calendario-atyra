from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.core.mail import send_mail
from .forms import AddClientForm
from .models import Reservas

from datetime import date, timedelta

def index(request):
    # CASAS ARE SAVED AS INTS NOW TO MAKE THINGS MORE SMOOTHLY WHEN QUERYING THE DB
    reserva_casas = [Reservas.objects.filter(fecha_inicio__lte=date.today() + timedelta(days=30)).exclude(fecha_fin__lt=date.today()).filter(casa=x + 1).order_by('fecha_fin') for x in range(3)]
    date_list = [date.today() + timedelta(days=x) for x in range(30)]
    
    # TODO: MAYBE AND JUST MAYBE TRY TO GET RID OF DIAS_OCUPADOS_CASAS 
    dias_ocupados_casas = [] # This one has all ocuppied days in the 3 houses
    for reservas in reserva_casas: # reserva_casas has 3 querysets
        dias_ocupados = [[], []] # The first list has the day, the second one has the Reservas instance
        for reserva in reservas: # Go through each queryset
            for i in range(int((reserva.fecha_fin - reserva.fecha_inicio).days) + 1):
                dias_ocupados[0].append(reserva.fecha_inicio + timedelta(days=i))
                dias_ocupados[1].append(reserva)
        print(dias_ocupados)
        dias_ocupados_casas.append(dias_ocupados)

    return render(request, 'calendarios/main.html', {'date_list':date_list, 'dias_ocupados_casas':dias_ocupados_casas})

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