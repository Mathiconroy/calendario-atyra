from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .forms import AddClientForm
from .models import Reservas

def index(request):
    reserva = Reservas.objects.filter()
    return render(request, 'calendarios/main.html', {'nombre':reserva[0].fecha_inicio})

def add_client_form(request):
    if request.method == "POST":
        form = AddClientForm(request.POST)
        if form.is_valid():
            # THIS IS EXTREMELY REDUNDANT, WRITE IT BETTER LATTER
            r = Reservas(casa=form.cleaned_data['casa'], nombre=form.cleaned_data['nombre'], cantidad_personas=form.cleaned_data['cantidad_personas'],
                        fecha_inicio=form.cleaned_data['fecha_inicio'], fecha_fin=form.cleaned_data['fecha_fin'], notas=form.cleaned_data['notas'])
            r.save()
            return render(request, 'calendarios/main.html')

    if request.method == "GET":
        form = AddClientForm()
        return render(request, 'calendarios/form.html', {'form':form})