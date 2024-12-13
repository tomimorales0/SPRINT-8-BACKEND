from django.urls import path
from .views import (
    ObtenerDatosClienteView,
    ObtenerSaldoCuentaView,
    ObtenerPrestamosClienteView,
    ObtenerPrestamosSucursalView,
    ObtenerTarjetasClienteView,
    GenerarSolicitudPrestamoView,
    AnularSolicitudPrestamoView,
    ModificarDireccionClienteView,
    ListarSucursalesView,
    UserRegistrationView,
    ObtenerMovimientosPorCuentaView,
    VerifyLoginView
)

urlpatterns = [
    path('cliente/datos/', ObtenerDatosClienteView.as_view(), name='obtener_datos_cliente'),
    path('cliente/saldo/', ObtenerSaldoCuentaView.as_view(), name='obtener_saldo_cuenta'),
    path('cliente/prestamos/', ObtenerPrestamosClienteView.as_view(), name='obtener_prestamos_cliente'),
    path('sucursal/prestamos/<int:sucursal_id>/', ObtenerPrestamosSucursalView.as_view(), name='obtener_prestamos_sucursal'),
    path('cliente/tarjetas/<int:cliente_id>/', ObtenerTarjetasClienteView.as_view(), name='obtener_tarjetas_cliente'),
    path('prestamo/solicitar/', GenerarSolicitudPrestamoView.as_view(), name='generar_solicitud_prestamo'),
    path('prestamo/anular/', AnularSolicitudPrestamoView.as_view(), name='anular_solicitud_prestamo'),
    path('cliente/modificar_direccion/', ModificarDireccionClienteView.as_view(), name='modificar_direccion_cliente'),
    path('sucursales/', ListarSucursalesView.as_view(), name='listar_sucursales'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('movimientos/', ObtenerMovimientosPorCuentaView.as_view(), name='movimientos_por_cuenta'),
    path('verify-login/', VerifyLoginView.as_view(), name='verify-login'),
]
