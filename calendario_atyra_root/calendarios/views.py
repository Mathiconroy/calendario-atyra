from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .forms import AddClientForm

def index(request):
    return render(request, 'calendarios/main.html')

def add_client_form(request):
    if request.method == "POST":
        form = AddClientForm(request.POST)
        if form.is_valid:
            # THIS IS EXTREMELY REDUNDANT, WRITE IT BETTER LATTER
            casa = form.cleaned_data['casa']
            nombre = form.cleaned_data['nombre']
            cantidad_personas = form.cleaned_data['cantidad_personas']
            fecha_inicio = form.cleaned_data['fecha_inicio']
            fecha_fin = form.cleaned_data['fecha_fin']
            notas = form.cleaned_data['notas']

            return render(request, 'calendarios/main.html')

    if request.method == "GET":
        form = AddClientForm()
        return render(request, 'calendarios/form.html', {'form':form})