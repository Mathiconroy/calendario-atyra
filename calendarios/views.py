# Django related imports
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.template.defaultfilters import date as _date
from django.template.loader import render_to_string
from django.contrib.staticfiles import finders
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
from django.core.mail import send_mail
from django.urls import reverse

# Modules from the project imports
from .forms import AddClientForm, ChangePaymentForm
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
tipos_adelanto = {0:'Giro', 1:'Depósito', 2:'Otro'}

def generate_rows(date_list, reservas):
    """
        date_list: A list of dates to render
        reservas: A QuerySet with all the reservas in the range of date_list
        returns: A dictionary with the date as the key and a list with 3 elements 
                    representing each cell in a line for the table (having None == No reservations for that house)
    """
    dias_ocupados = {}
    for day in date_list:
        dias_ocupados.update({day: [None, None, None]})
        for reserva in reservas:
            if reserva.fecha_inicio <= day <= reserva.fecha_fin:
                dias_ocupados[day][reserva.casa - 1] = reserva
    return dias_ocupados

def calculate_price(cantidad_adultos, cantidad_menores):
    """Returns the price based on the ammount of people given."""
    precio_adultos = 150000
    precio_menores = 120000
    precio_minimo = 450000
    total = cantidad_adultos * precio_adultos + cantidad_menores * precio_menores
    if total >= precio_minimo:
        precio = total
    else:
        precio = precio_minimo
    #f'{precio:,}'
    return precio

def remove_not_used_fields(all_fields):
    """Removes all unused fields from a dictionary with all the form fields."""
    not_used_fields = ("id", "edit", "confirm")
    for e in not_used_fields:
        all_fields.pop(e)

def send_confirmation_email(form_results):
    # TODO: Rework this, use form_results or the class.
    """Given the dictionary of the results of a form, it sends an email with all the data."""
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

def send_notice_reservation_email(form_results):
    # This works but TODO: next parameter in url in login doesn't work correctly
    send_mail(
        f'Pedido de reserva de {form_results["nombre"]}.',
        f'Se pidio una reserva para {_date(form_results["fecha_inicio"])} hasta {_date(form_results["fecha_fin"])}, haga click en el siguiente enlace para ver más información: {form_results["url"]}',
        os.environ.get('EMAIL_USERNAME', None),
        [os.environ.get('EMAIL_USERNAME', None)],
    )

def index(request):
    days_to_check_count = 120
    # CASAS ARE SAVED AS INTS NOW TO MAKE THINGS MORE SMOOTHLY WHEN QUERYING THE DB (AND MAKING IT SCALABLE)
    # reserva_casas = [Reservas.objects.filter(fecha_inicio__lte=date.today() + timedelta(days=days_to_check_count)).exclude(fecha_fin__lt=date.today()).filter(casa=x + 1).order_by('fecha_fin') for x in range(3)]
    reservas = Reservas.objects.filter(fecha_inicio__lte=date.today() + timedelta(days=days_to_check_count)).exclude(fecha_fin__lt=date.today()).order_by('fecha_inicio')
    date_list = [date.today() + timedelta(days=x) for x in range(days_to_check_count)]
    
    dias_ocupados_dict = generate_rows(date_list, reservas)

    return render(request, 'calendarios/main.html', {'date_list':date_list, 'dias_ocupados':dias_ocupados_dict})

def add_client_form(request):
    if request.method == "POST":
        form = AddClientForm(request.POST)
        if form.is_valid():
            form_results = form.clean() # This is here to validate again with my custom clean() method in forms.py
            if form_results['confirm'] == False:
                form_results['confirm'] = True
                form = AddClientForm(initial={
                    'nombre': form_results['nombre'],
                    'casa': form_results['casa'],
                    'email': form_results['email'],
                    'cantidad_adultos': form_results['cantidad_adultos'],
                    'fecha_inicio': form_results['fecha_inicio'],
                    'fecha_fin': form_results['fecha_fin'],
                    'notas': form_results['notas'],
                    'edit': form_results['edit'],
                    'confirm': form_results['confirm'],
                    'tipo_adelanto': form_results['tipo_adelanto'],
                }) # If defining the dictionary it works for some reason???
                # TODO: FOR SOME REASON THE CONFIRM FIELD DOESNT GET SET TO TRUE IF I DO INITIAL=FORM_RESULTS
                messages.add_message(request, messages.WARNING, 'Debe confirmar la reserva', extra_tags="alert alert-warning text-center")
                precio = calculate_price(int(form_results['cantidad_adultos']), int(form_results['cantidad_menores']))
                remove_not_used_fields(form_results)        
                return render(request, 'calendarios/form.html', {
                    'form':form,
                    'form_results':form_results, 
                    'confirm':True, 
                    'precio':f'{precio:,}'.replace(',', '.'),
                    'reserva_length':(form_results['fecha_fin'] - form_results['fecha_inicio']).days,
                })
                # f'{precio:,}' Use this to render price in text form
            else:
                r = Reservas(
                    casa=form_results['casa'], 
                    nombre=form_results['nombre'], 
                    email=form_results['email'], 
                    cantidad_adultos=form_results['cantidad_adultos'], 
                    cantidad_menores=form_results['cantidad_menores'],
                    cantidad_gratis=form_results['cantidad_gratis'],
                    fecha_inicio=form_results['fecha_inicio'],
                    fecha_fin=form_results['fecha_fin'], 
                    notas=form_results['notas'],
                    tipo_adelanto=form_results['tipo_adelanto'],
                    precio=calculate_price(int(form_results['cantidad_adultos']), int(form_results['cantidad_menores'])),
                )
                if request.user.is_authenticated:
                    r.estado = 1
                    messages.add_message(request, messages.SUCCESS, 'Reserva añadida', extra_tags="alert alert-success text-center")
                    # NOTE: Is this necessary?
                    #if form_results['email']:
                        #send_confirmation_email(form_results)
                else:
                    r.estado = 0
                    form_results['url'] = request.build_absolute_uri('/view_client_form/' + str(r.id))
                    send_notice_reservation_email(form_results)
                    messages.add_message(request, messages.SUCCESS, 'Reserva pedida', extra_tags="alert alert-success text-center")
                r.save()
                return redirect('index')

    if request.method == "GET":
        form = AddClientForm(initial={'edit':False})
        
    return render(request, 'calendarios/form.html', {'form':form, 'confirm':False})

@login_required
def view_client_form(request, id):
    reserva = get_object_or_404(Reservas, id=id)
    casa = casas[int(reserva.casa)]
    estado = reserva.get_estado_display()
    tipo_adelanto = reserva.get_tipo_adelanto_display()
    return render(request, 'calendarios/view_form.html', {'reserva':reserva, 'casa':casa, 'estado':estado, 'tipo_adelanto':tipo_adelanto})

@login_required
def edit_client_form(request, id):
    if request.method == "POST":
        form = AddClientForm(request.POST)
        if form.is_valid():
            form = form.clean() # This is here to validate again with my custom clean() method in forms.py
            remove_not_used_fields(form)
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
            'cantidad_personas':reserva.cantidad_adultos,
            'cantidad_menores':reserva.cantidad_menores,
            'cantidad_gratis':reserva.cantidad_gratis,
            'fecha_inicio':reserva.fecha_inicio,
            'fecha_fin':reserva.fecha_fin,
            'notas':reserva.notas,
            'edit':True
        })
    return render(request, 'calendarios/edit_form.html', {'form':form, 'id':id})

@login_required
def confirm_reservation(request, id):
    # TODO: Maybe show an error if it was already updated?
    r = Reservas.objects.get(id=id)
    if r.estado == 0:
        r.estado = 1
        r.save()
        messages.add_message(request, messages.SUCCESS, 'Reserva confirmada', extra_tags="alert alert-success text-center")
        # TODO: This
        #send_confirmation_email()
    else:
        messages.add_message(request, messages.WARNING, 'La reserva ya estaba confirmada', extra_tags="alert alert-warning text-center")
    return redirect('index')

@login_required
def search_reservation(request):
    return render(request, 'search_reservations.html')

@login_required
def change_payment(request, id):
    r = Reservas.objects.get(id=id)
    if request.method == "POST":
        form = ChangePaymentForm(request.POST)
        if form.is_valid():
            r.deposito = int(form.cleaned_data['cantidad_deposito'])
            r.save()
            messages.add_message(request, messages.SUCCESS, 'Seña cambiada', extra_tags="alert alert-success text-center")
            return redirect('index')

    if request.method == "GET":
        form = ChangePaymentForm(initial={'id':id, 'cantidad':r.deposito})

    return render(request, 'calendarios/change_payment_form.html', {'form':form, 'reserva':r, 'saldo':f'{r.precio - r.deposito:,}', 'precio':f'{r.precio:,}'})

@login_required
def delete_reservation(request, id):
    Reservas.objects.filter(id=id).delete()
    return redirect('index')

@login_required
def view_reservation_requests(request):
    r = Reservas.objects.filter(estado=0).order_by('fecha_inicio')
    print(r)
    return render(request, 'calendarios/view_reservation_requests.html', {'reservas':r})

@login_required
def test_mail(request):
    return render(request, 'calendarios/mail_template.html')

@login_required
def logout(request):
    return logout_then_login(request)