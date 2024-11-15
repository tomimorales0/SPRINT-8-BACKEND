from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=80)
    apellido = models.CharField(max_length=80)
    DNI = models.CharField(max_length=20)
    telefono = models.CharField(max_length=15)
    tipo = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        db_table = 'Clientes'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'