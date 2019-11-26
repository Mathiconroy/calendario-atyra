from django.db import models

class Reservas(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateField(blank=False)
    notas = models.TextField()

    def __str__(self):
        return self.nombre
