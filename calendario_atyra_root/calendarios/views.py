from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def index(request):
    return render(request, 'calendarios/main.html')

# Create your views here.
