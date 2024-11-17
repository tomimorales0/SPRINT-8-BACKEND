from django.db import models
from sucursal.models import Sucursal

class Empleado(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    nombre= models.CharField(max_length=20, unique=True)
    apellido= models.CharField(max_length=50)
    DNI = models.CharField(max_length=8)
    fecha_contratacion = models.DateField()

    def __str__(self):
        return f"Empleado {self.nombre} {self.apellido} - Sucursal {self.sucursal}"

    class Meta:
        db_table = 'Empleados'
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'