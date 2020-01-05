from django.contrib import admin
from .models import Reservas

class PageAdmin(admin.ModelAdmin): #TODO: This?
    pass

admin.site.register(Reservas, PageAdmin)