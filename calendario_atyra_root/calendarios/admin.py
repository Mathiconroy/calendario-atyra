from django.contrib import admin
from .models import Reservas

class PageAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha')
    ordering = ('fecha',)
    search_fields = ('nombre', 'fecha')

admin.site.register(Reservas, PageAdmin)