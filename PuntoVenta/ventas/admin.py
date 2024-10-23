from django.contrib import admin
from ventas.models import Cliente, Producto, Usuario

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nit_Cui', 'correoElectronico', 'direccion', 'estado')
    search_fields = ['nombre', 'Nit / Cui']
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
admin.site.register(Cliente, ClienteAdmin)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion', 'precio_unitario')
    search_fields = ['descripcion']
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
admin.site.register(Producto, ProductoAdmin)

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correoElectronico', 'estado', 'rol', 'clave')
    search_fields = ['nombre']
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
admin.site.register(Usuario, UsuarioAdmin)
