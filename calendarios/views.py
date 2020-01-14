# Django related imports
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.core.mail import send_mail, EmailMessage
from django.template.defaultfilters import date as _date
from django.template.loader import render_to_string

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

casas = {1:'Barro Roga', 2:'Ysypo Roga', 3:'Hierro Roga'}

def send_confirmation_email(form_results=None):
    msgRoot = MIMEMultipart('related')
    msgRoot['From'] = 'mathias.martinez018@gmail.com'
    msgRoot['To'] = 'mathias.martinez018@gmail.com'
    msgRoot['Subject'] = 'AtyRoga - Reserva hecha'

    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    msgText = MIMEText('Su reserva se ha hecho, felicidades!')
    msgAlternative.attach(msgText)

    msgText = MIMEText(render_to_string('calendarios/mail_template.html'), 'html')
    msgAlternative.attach(msgText)
    
    import os
    import sys
    dir_path = os.path.dirname(os.path.realpath(__file__))
    mypngfile = os.path.join(dir_path, "AtyRogaLogo.png")
    imgFile = open(mypngfile, 'rb') # TODO: If this works, change the path
    msgImage = MIMEImage(imgFile.read()) # TODO: DONT FORGET TO CHANGE THE PATH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    imgFile.close()

    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)

    smtp = smtplib.SMTP('smtp.gmail.com:587')
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login('mathias.martinez018@gmail.com', 'AsdfOwoOmg123456')
    smtp.sendmail('mathias.martinez018@gmail.com', 'mathias.martinez018@gmail.com', msgRoot.as_string())
    smtp.quit()

def index(request):
    # TODO: Make the email stuff
    # CASAS ARE SAVED AS INTS NOW TO MAKE THINGS MORE SMOOTHLY WHEN QUERYING THE DB (AND MAKING IT SCALABLE)
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
        # print(dias_ocupados) for debugging
        dias_ocupados_casas.append(dias_ocupados)

    return render(request, 'calendarios/main.html', {'date_list':date_list, 'dias_ocupados_casas':dias_ocupados_casas})

def add_client_form(request):
    if request.method == "POST":
        form = AddClientForm(request.POST)
        if form.is_valid():
            form = form.clean() # This is here to validate again with my custom clean() method in forms.py
            r = Reservas(casa=form['casa'], nombre=form['nombre'], email=form['email'], 
                        cantidad_personas=form['cantidad_personas'], fecha_inicio=form['fecha_inicio'],
                        fecha_fin=form['fecha_fin'], notas=form['notas'])
            r.save()
            print(form['casa'])
            if form['email']: # TODO: Finish this
                send_mail('Atyroga - Reserva hecha', 
                            f"""Buenas tardes, {form['nombre']}.\n
                            Su reserva se ha realizado para la casa {casas[int(form['casa'])]}, iniciando el {_date(form['fecha_inicio'])}hasta {_date(form['fecha_fin'])}""",
                            'mathias.martinez018@gmail.com', [form['email']])
            return redirect('index')

    if request.method == "GET":
        form = AddClientForm()

    return render(request, 'calendarios/form.html', {'form':form})

def view_client_form(request, id):
    reserva = Reservas.objects.get(id=id)
    return render(request, 'calendarios/view_form.html', {'reserva':reserva})

def test_mail(request): # TODO: Make this shit LOOKUP EMAILMESSAGE CLASS
#    send_mail('Atyroga - Reserva hecha', # Put {} for name and cantidad_personas, maybe add a way to show the final price?
#                f"""Buenas tardes, Mathias Martinez.\n
#Su reserva para 5 personas se ha realizado para la casa {casas[2]}, iniciando el {_date(date.today())} hasta el {_date(date.today())}.""",
#'mathias.martinez018@gmail.com', ['mathias.martinez018@gmail.com'], html_message=render_to_string('calendarios/mail_template.html'))
    email = EmailMessage()
    send_confirmation_email()
    return render(request, 'calendarios/mail_template.html')