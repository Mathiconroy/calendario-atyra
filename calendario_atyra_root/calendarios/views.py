from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def index(request):
    return render(request, 'calendarios/main.html')

def add_client_form(request):
    return render(request, 'calendarios/form.html')