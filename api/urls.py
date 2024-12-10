from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, CuentaViewSet, PrestamoViewSet, TarjetaViewSet

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'cuentas', CuentaViewSet)
router.register(r'prestamos', PrestamoViewSet)
router.register(r'tarjetas', TarjetaViewSet)

urlpatterns = router.urls
