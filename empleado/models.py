from django.db import models
from django.contrib.auth.models import User
from sucursal.models import Sucursal

class Empleado(models.Model):
    # Relación OneToOne con User (esto permite asociar un usuario de Django a un empleado)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='empleado', null=True, blank=True)
    
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=20, unique=True)
    apellido = models.CharField(max_length=50)
    DNI = models.CharField(max_length=8)
    fecha_contratacion = models.DateField()

    def __str__(self):
        return f"Empleado {self.nombre} {self.apellido} - Sucursal {self.sucursal}"

    class Meta:
        db_table = 'Empleados'
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'