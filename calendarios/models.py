from django.db import models

class Reservas(models.Model):
    casa = models.IntegerField(null=False)
    nombre = models.CharField(null=False, max_length=150)
    email = models.EmailField(null=True)
    cantidad_personas = models.IntegerField(null=False)
    fecha_inicio = models.DateField(null=False)
    fecha_fin = models.DateField(null=False)
    notas = models.TextField()

    def __str__(self):
        return f"ID: {self.id}, Nombre: {self.nombre}, Casa: {self.casa} {self.fecha_inicio.strftime('%d/%m/%Y')} - {self.fecha_fin.strftime('%d/%m/%Y')}"
