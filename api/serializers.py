from rest_framework import serializers
from clientes.models import Cliente
from cuentas.models import Cuenta
from prestamos.models import Prestamo
from tarjetas.models import Tarjeta
from sucursal.models import Sucursal
from django.contrib.auth.models import User
from movimientos.models import Movimiento

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
    
class TransferenciaSerializer(serializers.Serializer):
    destinatario_id = serializers.IntegerField()
    monto = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate(self, data):
        # Validaciones adicionales si es necesario
        if data['monto'] <= 0:
            raise serializers.ValidationError("El monto debe ser positivo.")
        return data

    def validate_destinatario_id(self, value):
        try:
            # Validamos que el destinatario exista
            destinatario = Cliente.objects.get(id=value)
        except Cliente.DoesNotExist:
            raise serializers.ValidationError("Destinatario no encontrado.")
        return destinatario

class MovimientoSerializer(serializers.ModelSerializer):
    # Mostrar el nombre de la cuenta
    cuenta = serializers.StringRelatedField()
    # Mostrar el nombre del destinatario
    destinatario = serializers.StringRelatedField(required=False)

    class Meta:
        model = Movimiento
        fields = ['cuenta', 'fecha', 'tipo_movimiento', 'monto', 'destinatario']

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'apellido', 'DNI', 'tipo', 'sucursal']

class CuentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuenta
        fields = ['numero_cuenta', 'tipo', 'saldo', 'cliente']

class PrestamoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestamo
        fields = ['tipo_prestamo', 'fecha_inicio', 'monto', 'aprobado']

class TarjetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarjeta
        fields = ['numero_tarjeta', 'tipo_tarjeta', 'fecha_expiracion']

class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = ['nombre', 'direccion']