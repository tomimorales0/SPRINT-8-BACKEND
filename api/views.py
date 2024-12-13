from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from clientes.models import Cliente
from cuentas.models import Cuenta
from prestamos.models import Prestamo
from tarjetas.models import Tarjeta
from sucursal.models import Sucursal
from .serializers import ClienteSerializer, CuentaSerializer, PrestamoSerializer, TarjetaSerializer, SucursalSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authentication import BasicAuthentication
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer, MovimientoSerializer, TransferenciaSerializer
from rest_framework.views import APIView
from movimientos.models import Movimiento
import uuid
from django.db import transaction


class TransferenciaAPIView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Obtener el cliente autenticado
        cliente_origen = Cliente.objects.get(user=request.user)  # Obtiene el cliente basado en el usuario autenticado
        cuenta_origen = Cuenta.objects.get(cliente=cliente_origen)

        # Deserializar los datos de la transferencia
        serializer = TransferenciaSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Obtener los datos validados
                destinatario_cliente = serializer.validated_data['destinatario_id']
                monto = serializer.validated_data['monto']

                # Verificar si el destinatario existe
                destinatario = Cliente.objects.get(id=destinatario_cliente.id)
                cuenta_destino = Cuenta.objects.get(cliente=destinatario)

                # Verificar que la cuenta de origen tenga suficiente saldo
                if cuenta_origen.saldo < monto:
                    return Response({'error': 'Saldo insuficiente'}, status=status.HTTP_400_BAD_REQUEST)

                # Iniciar transacción para asegurar que la transferencia sea atómica
                with transaction.atomic():
                    # Realizar la transferencia
                    cuenta_origen.saldo -= monto
                    cuenta_destino.saldo += monto
                    cuenta_origen.save()
                    cuenta_destino.save()

                   
                    Movimiento.objects.create(
                        cuenta=cuenta_origen,
                        tipo_movimiento='Salida',
                        monto=monto,
                        destinatario=destinatario
                    )
                    

                return Response({'message': 'Transferencia realizada con éxito'}, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




TOKENS = {}
#generador de tokens
class GenerateTokenView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        token = str(uuid.uuid4())  # Generar un token único
        TOKENS[user.username] = token  # Guardar el token asociado al usuario
        return Response({'token': token}, status=200)
    
#verificador de basic auth
class VerifyLoginView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        return Response({'message': f'Bienvenido, {user.username}!'}, status=200)


class UserRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
             # Guardamos el usuario si los datos son válidos
            serializer.save()
            return Response({"message": "Usuario registrado exitosamente"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Movimientos por cuentas
class ObtenerMovimientosPorCuentaView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Verificar que no sea superusuario/empleado
        if request.user.is_superuser:
            return Response({"detail": "No tienes permisos para acceder a esta información."}, status=status.HTTP_403_FORBIDDEN)
        # Obtener el cliente actual desde el usuario autenticado
        cliente = Cliente.objects.get(user=request.user)  # Se obtiene el cliente basado en el usuario autenticado
        # Obtener las cuentas asociadas al cliente
        cuentas = cliente.cuenta_set.all()

        # Obtener los movimientos para todas las cuentas del cliente
        movimientos = Movimiento.objects.filter(cuenta__in=cuentas).order_by('-fecha')
        
        if not movimientos.exists():
            return Response(
                {"mensaje": "No hay movimientos para las cuentas del cliente."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Serializar los movimientos
        serializer = MovimientoSerializer(movimientos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Obtener datos de un cliente
class ObtenerDatosClienteView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Verificar que no sea superusuario/empleado
        if request.user.is_superuser:
            return Response({"detail": "No tienes permisos para acceder a esta información."}, status=status.HTTP_403_FORBIDDEN)
        
        cliente = Cliente.objects.get(user=request.user)
        serializer = ClienteSerializer(cliente)
        return Response(serializer.data)

# Obtener saldo de cuenta de un cliente
class ObtenerSaldoCuentaView(APIView):
    
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request, *args, **kwargs):
        # Verificar que no sea superusuario/empleado
        if request.user.is_superuser:
            return Response({"detail": "No tienes permisos para acceder a esta información."}, status=status.HTTP_403_FORBIDDEN)

        cliente = Cliente.objects.get(user=request.user)
        cuenta = Cuenta.objects.get(cliente=cliente)
        serializer = CuentaSerializer(cuenta)
        return Response(serializer.data)

# Obtener monto de préstamos de un cliente
class ObtenerPrestamosClienteView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Verificar que no sea superusuario/empleado
        if request.user.is_superuser:
            return Response({"detail": "No tienes permisos para acceder a esta información."}, status=status.HTTP_403_FORBIDDEN)

        cliente = Cliente.objects.get(user=request.user)
        prestamos = Prestamo.objects.filter(cliente=cliente)
        serializer = PrestamoSerializer(prestamos, many=True)
        return Response(serializer.data)

# Obtener monto de préstamos de una sucursal (solo para empleados/superusuarios)
class ObtenerPrestamosSucursalView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Verificar si es un superusuario (empleado)
        if request.user.is_superuser:
            sucursal_id = kwargs.get('sucursal_id')
            prestamos = Prestamo.objects.filter(cliente__sucursal_id=sucursal_id)
            serializer = PrestamoSerializer(prestamos, many=True)
            return Response(serializer.data)
        
        return Response({"detail": "No tienes permisos para acceder a esta información."}, status=status.HTTP_403_FORBIDDEN)

# Obtener tarjetas asociadas a un cliente (solo para empleados)
class ObtenerTarjetasClienteView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Verificar si es un superusuario (empleado)
        if request.user.is_superuser:
            cliente_id = kwargs.get('cliente_id')
            tarjetas = Tarjeta.objects.filter(cliente_id=cliente_id)
            serializer = TarjetaSerializer(tarjetas, many=True)
            return Response(serializer.data)
        
        return Response({"detail": "No tienes permisos para acceder a esta información."}, status=status.HTTP_403_FORBIDDEN)

# Generar una solicitud de préstamo para un cliente (solo para empleados)
class GenerarSolicitudPrestamoView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Verificar si es un superusuario (empleado)
        if request.user.is_superuser:
            cliente_id = request.data.get('cliente_id')
            monto = request.data.get('monto')
            tipo_prestamo = request.data.get('tipo_prestamo')

            cliente = Cliente.objects.get(id=cliente_id)
            prestamo = Prestamo.objects.create(cliente=cliente, monto=monto, tipo_prestamo=tipo_prestamo, aprobado=False)
            return Response({"detail": "Solicitud de préstamo generada correctamente."}, status=status.HTTP_201_CREATED)
        
        return Response({"detail": "No tienes permisos para realizar esta acción."}, status=status.HTTP_403_FORBIDDEN)

# Anular solicitud de préstamo de un cliente (solo para empleados)
class AnularSolicitudPrestamoView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Verificar si es un superusuario (empleado)
        if request.user.is_superuser:
            prestamo_id = request.data.get('prestamo_id')
            prestamo = Prestamo.objects.get(id=prestamo_id)
            prestamo.aprobado = False
            prestamo.save()
            return Response({"detail": "Solicitud de préstamo anulada correctamente."}, status=status.HTTP_200_OK)
        
        return Response({"detail": "No tienes permisos para realizar esta acción."}, status=status.HTTP_403_FORBIDDEN)


# Modificar dirección de un cliente (clientes y empleados pueden modificar)
class ModificarDireccionClienteView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados

    def post(self, request, *args, **kwargs):
        try:
            # Obtener el cliente asociado al usuario autenticado
            cliente = Cliente.objects.get(user=request.user)

            # Obtener y modificar la dirección de la sucursal
            nueva_direccion = request.data.get('direccion')
            if nueva_direccion:
                cliente.sucursal.direccion = nueva_direccion
                cliente.sucursal.save()
                return Response({"detail": "Dirección modificada correctamente."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "La dirección no puede estar vacía."}, status=status.HTTP_400_BAD_REQUEST)

        except Cliente.DoesNotExist:
            return Response({"detail": "Cliente no encontrado."}, status=status.HTTP_404_NOT_FOUND)

# Listado de todas las sucursales (endpoint público)
class ListarSucursalesView(APIView):
    authentication_classes = []  # Desactiva autenticación para esta vista
    permission_classes = [AllowAny]  # Permite acceso a cualquier usuario

    def get(self, request, *args, **kwargs):
        sucursales = Sucursal.objects.all()
        serializer = SucursalSerializer(sucursales, many=True)
        return Response(serializer.data)