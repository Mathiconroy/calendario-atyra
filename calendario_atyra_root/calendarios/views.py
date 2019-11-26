from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def index(request):
    return HttpResponse('<b>Hello World!</b>')

# Create your views here.
