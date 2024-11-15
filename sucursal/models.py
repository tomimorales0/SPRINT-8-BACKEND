from django.db import models


class Sucursal (models.Model):
    nombre = models.CharField(max_length=20)
    direccion = models.CharField(max_length=60, unique=True)
   
    def __str__(self):
        return f"Sucursal {self.nombre} Direccion: {self.direccion}"

    class Meta:
        db_table = 'Sucursales'
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'   