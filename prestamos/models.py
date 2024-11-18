from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    USER_TYPES = [
        ('BLACK', 'Black'),
        ('GOLD', 'Gold'),
        ('CLASSIC', 'Classic'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=USER_TYPES)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.user.username} - {self.tipo}"

class Prestamo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo_prestamo = models.CharField(max_length=100, null=False, default= 'Classic')
    fecha_inicio = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    aprobado = models.BooleanField(default=False)

    def __str__(self):
        return f"Préstamo de {self.cliente.user.username} - {self.monto}"