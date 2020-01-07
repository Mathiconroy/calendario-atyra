from django.db import models

class Reservas(models.Model): # THE ID FIELD IS ADDED AUTOMATICALLY
    id = models.IntegerField(primary_key=True)
    casa = models.CharField(null=False, max_length=5)
    nombre = models.CharField(null=False, max_length=150)
    cantidad_personas = models.IntegerField(null=False)
    fecha_inicio = models.DateField(null=False)
    fecha_fin = models.DateField(null=False)
    notas = models.TextField()

    def __str__(self):
        return self.nombre
