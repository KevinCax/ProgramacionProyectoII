from django.urls import path
from . import views
from .views import cerrar_sesion


urlpatterns = [
    path('', views.inicio_view, name='Inicio'),
    path('iniciar-sesion/', views.login_view, name='Login'),
    path('cerrar-sesion/', cerrar_sesion, name='CerrarSesion'),
    path('logout/', views.logout_view, name='CrearCuenta'),
    path('clientes/', views.clientes_view, name='Clientes'),
    path('add_cliente/', views.add_cliente_view, name='AddCliente'),
    path('edit_cliente/', views.edit_cliente_view, name='EditCliente'),
    path('delete_cliente/', views.delete_cliente_view, name='DeleteCliente'),
    path('productos/', views.productos_view, name='Productos'),
    path('add_producto/', views.add_producto_view, name='AddProducto'),
    path('delete_producto/', views.delete_producto_view, name='DeleteProducto'),
    path('edit_producto/', views.edit_producto_view, name='EditProducto'),
    path('ventas/', views.ventas_view, name='Ventas'),
    path('add_ventas/',views.add_ventas.as_view(), name='AddVenta'),
    path('export/', views.export_pdf_view, name="ExportPDF" ),
    path('export/<id>/<iva>', views.export_pdf_view, name="ExportPDF" ),
    path('usuarios/', views.usuarios_view, name='Usuarios'),
    path('add_usuario/', views.add_usuarios_view, name='AddUsuario'),
    path('edit_usuario/', views.edit_usuario_view, name='EditUsuario'),
    path('toggle_usuario_estado/', views.toggle_usuario_estado, name='ActivarDesactivar'),
    
]