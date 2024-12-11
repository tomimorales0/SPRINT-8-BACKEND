from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from clientes.models import Cliente
from cuentas.models import Cuenta
from prestamos.models import Prestamo
from tarjetas.models import Tarjeta
from .serializers import ClienteSerializer, CuentaSerializer, PrestamoSerializer, TarjetaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer

class UserRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
             # Guardamos el usuario si los datos son válidos
            serializer.save()
            return Response({"message": "Usuario registrado exitosamente"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClienteViewSet(ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]

class CuentaViewSet(ModelViewSet):
    queryset = Cuenta.objects.all()
    serializer_class = CuentaSerializer
    permission_classes = [IsAuthenticated]

class PrestamoViewSet(ModelViewSet):
    queryset = Prestamo.objects.all()
    serializer_class = PrestamoSerializer
    permission_classes = [IsAuthenticated]

class TarjetaViewSet(ModelViewSet):
    queryset = Tarjeta.objects.all()
    serializer_class = TarjetaSerializer
    permission_classes = [IsAuthenticated]
