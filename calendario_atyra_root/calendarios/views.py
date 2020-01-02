from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .forms import AddClientForm

def index(request):
    return render(request, 'calendarios/main.html')

def add_client_form(request):
    if request.method == "POST":
        form = AddClientForm(request.POST)
        if form.is_valid:
            return render(request, 'calendarios/main.html')

    if request.method == "GET":
        form = AddClientForm()
        return render(request, 'calendarios/form.html', {'form':form})