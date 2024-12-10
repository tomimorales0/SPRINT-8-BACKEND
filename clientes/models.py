from django.db import models
from sucursal.models import Sucursal
from django.contrib.auth.models import User



class Cliente(models.Model):
    USER_TYPES = [
        ('BLACK', 'Black'),
        ('GOLD', 'Gold'),
        ('CLASSIC', 'Classic'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=80)
    apellido = models.CharField(max_length=80)
    DNI = models.CharField(max_length=20)
    tipo = models.CharField(max_length=10, choices=USER_TYPES)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        db_table = 'Clientes'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'