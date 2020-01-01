from django.db import models

class Reservas(models.Model):
    casa = models.CharField(max_length=5)
    nombre = models.CharField(max_length=100)
    cantidad_personas = models.CharField(max_length=5)
    fecha = models.DateField(blank=False)
    notas = models.TextField()

    def __str__(self):
        return self.nombre
