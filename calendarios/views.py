# Django related imports
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.template.defaultfilters import date as _date
from django.template.loader import render_to_string
from django.contrib.staticfiles import finders
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login

# Modules from the project imports
from .forms import AddClientForm
from .models import Reservas

# Email related imports (not Django)
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib

# Other imports
from datetime import date, timedelta
import os

casas = {1:'Barro Roga', 2:'Ysypo Roga', 3:'Hierro Roga'}

def send_confirmation_email(form_results):
    EMAIL_USERNAME = os.environ.get('EMAIL_USERNAME', None)
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', None)
    if EMAIL_PASSWORD is None or EMAIL_USERNAME is None:
        return

    msgRoot = MIMEMultipart('related')
    msgRoot['From'] = EMAIL_USERNAME
    msgRoot['To'] = EMAIL_PASSWORD
    msgRoot['Subject'] = 'AtyRoga - Reserva hecha'

    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    msgText = MIMEText(f'Buenas, {form_results["nombre"]}.\nSu reserva para {form_results["cantidad_personas"]} persona(s) se ha realizado para la casa {casas[int(form_results["casa"])]}, iniciando el {_date(form_results["fecha_inicio"])} hasta el {_date(form_results["fecha_fin"])}.\nGracias por la confianza.\nEste correo se ha enviado de forma automática.')
    msgAlternative.attach(msgText)

    msgText = MIMEText(render_to_string('calendarios/mail_template.html', context={'form':form_results, 'casa':casas[int(form_results['casa'])]}), 'html')
    msgAlternative.attach(msgText)
    
    logo_path = finders.find('calendarios/AtyRoga_Logo.png')
    imgFile = open(logo_path, 'rb')
    msgImage = MIMEImage(imgFile.read())
    imgFile.close()

    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)

    smtp = smtplib.SMTP('smtp.gmail.com:587')
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(EMAIL_USERNAME, EMAIL_PASSWORD)
    smtp.sendmail(EMAIL_USERNAME, form_results['email'], msgRoot.as_string())
    smtp.quit()

def index(request):
    days_to_check_count = 120
    # CASAS ARE SAVED AS INTS NOW TO MAKE THINGS MORE SMOOTHLY WHEN QUERYING THE DB (AND MAKING IT SCALABLE)
    reserva_casas = [Reservas.objects.filter(fecha_inicio__lte=date.today() + timedelta(days=days_to_check_count)).exclude(fecha_fin__lt=date.today()).filter(casa=x + 1).order_by('fecha_fin') for x in range(len(casas))]
    date_list = [date.today() + timedelta(days=x) for x in range(days_to_check_count)]
    
    # TODO: MAYBE AND JUST MAYBE TRY TO GET RID OF DIAS_OCUPADOS_CASAS 
    dias_ocupados_casas = [] # This one has all ocuppied days in the 3 houses
    for reservas in reserva_casas: # reserva_casas has 3 querysets
        dias_ocupados = [[], []] # The first list has the day, the second one has the Reservas instance
        for reserva in reservas: # Go through each queryset
            for i in range(int((reserva.fecha_fin - reserva.fecha_inicio).days) + 1):
                dias_ocupados[0].append(reserva.fecha_inicio + timedelta(days=i))
                dias_ocupados[1].append(reserva)
        # print(dias_ocupados) for debugging
        dias_ocupados_casas.append(dias_ocupados)

    return render(request, 'calendarios/main.html', {'date_list':date_list, 'dias_ocupados_casas':dias_ocupados_casas})

@login_required
def add_client_form(request):
    if request.method == "POST":
        form = AddClientForm(request.POST)
        if form.is_valid():
            form = form.clean() # This is here to validate again with my custom clean() method in forms.py
            r = Reservas(casa=form['casa'], nombre=form['nombre'], email=form['email'], 
                        cantidad_personas=form['cantidad_personas'], fecha_inicio=form['fecha_inicio'],
                        fecha_fin=form['fecha_fin'], notas=form['notas'])
            r.save()
            if form['email']:
                send_confirmation_email(form)
            messages.add_message(request, messages.SUCCESS, 'Reserva añadida', extra_tags="alert alert-success text-center")
            return redirect('index')

    if request.method == "GET":
        form = AddClientForm(initial={'edit':False})
    return render(request, 'calendarios/form.html', {'form':form})

@login_required
def view_client_form(request, id):
    reserva = get_object_or_404(Reservas, id=id)
    casa = casas[int(reserva.casa)]
    return render(request, 'calendarios/view_form.html', {'reserva':reserva, 'casa':casa})

@login_required
def edit_client_form(request, id):
    if request.method == "POST":
        form = AddClientForm(request.POST)
        if form.is_valid():
            form = form.clean() # This is here to validate again with my custom clean() method in forms.py
            for e in ['cantidad_dias', 'edit']:
                form.pop(e)
            form['casa'] = int(form['casa'])
            r = Reservas.objects.filter(id=id).update(**form)
            messages.add_message(request, messages.SUCCESS, 'Reserva editada', extra_tags="alert alert-success text-center")
            return redirect('index')
    
    if request.method == "GET":
        reserva = Reservas.objects.get(id=id)
        form = AddClientForm(initial={
            'id':reserva.id,
            'casa':str(reserva.casa),
            'nombre':reserva.nombre,
            'email':reserva.email,
            'cantidad_personas':reserva.cantidad_personas,
            'fecha_inicio':reserva.fecha_inicio,
            'fecha_fin':reserva.fecha_fin,
            'cantidad_dias':(reserva.fecha_fin - reserva.fecha_inicio).days,
            'notas':reserva.notas,
            'edit':True
        })
    return render(request, 'calendarios/edit_form.html', {'form':form, 'id':id})

@login_required
def test_mail(request):
    send_confirmation_email()
    return render(request, 'calendarios/mail_template.html')

def logout(request):
    return logout_then_login(request)