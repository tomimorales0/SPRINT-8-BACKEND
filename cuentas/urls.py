from django.urls import path
from .views import CuentaCreateView

urlpatterns = [
    path('crear/', CuentaCreateView.as_view(), name='crear_cuenta'),
]
