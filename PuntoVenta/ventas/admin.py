from django.contrib import admin
from ventas.models import Cliente, Producto

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nit', 'cui', 'nombre', 'telefono')
    search_fields = ['nombre']
    readonly_fields = ('create', 'update')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
admin.site.register(Cliente, ClienteAdmin)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion', 'precio_unitario')
    search_fields = ['descripcion']
    readonly_fields = ('create', 'update')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
admin.site.register(Producto, ProductoAdmin)