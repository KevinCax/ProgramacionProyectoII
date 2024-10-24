from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Producto, Usuario, Egreso, ProductosEgreso
from .forms import AddClienteForm, EditarClienteForm, AddProductoForm, EditarProductoForm, AddUsuarioForm, EditarUsuarioForm
from django.contrib import messages
from django.views.generic import ListView
from django.http import JsonResponse, HttpResponse
from django.template.loader import get_template
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
from django.conf import settings
import os
from django.db import IntegrityError
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect



# Vistas Clientes.

def inicio_view(request):
    
    return render(request, 'inicio.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = Usuario.objects.get(correoElectronico=email)
            user = authenticate(request, username=user.usuario, password=password)
        except Usuario.DoesNotExist:
            user = None
        
        if user is not None:
            login(request, user)
            return redirect('Login')
        else:
            messages.error(request, 'Credenciales incorrectas.')
    
    return render(request, 'signin.html')
        
    
        

def logout_view(request):
    return render(request, 'logout.html')

def cerrar_sesion(request):
    logout(request)
    return redirect('Inicio') 

def clientes_view(request):
    clientes = Cliente.objects.all()
    form_personal = AddClienteForm()
    form_editar = EditarClienteForm()
    
    context = {
        'clientes': clientes,
        'form_personal': form_personal,
        'form_editar': form_editar
    }
    return render(request, 'clientes.html', {'clientes': clientes, 'form_personal': form_personal, 'form_editar': form_editar, 'user': request.user})


def add_cliente_view(request):
    if request.method == 'POST':
        form = AddClienteForm(request.POST)
        
        if form.is_valid():
            nit_Cui_dpi = form.cleaned_data.get('nit_Cui')

            nit_Cui_dpi_sin_guiones = nit_Cui_dpi.replace("-", "").replace(" ", "")
            if len(nit_Cui_dpi_sin_guiones) == 13:
                if not validar_dpi(nit_Cui_dpi_sin_guiones):
                    messages.error(request, "DPI inválido")
                    return redirect('Clientes')
                
            elif len(nit_Cui_dpi_sin_guiones) >= 8 and len(nit_Cui_dpi_sin_guiones) <= 10:
                if not validar_nit(nit_Cui_dpi_sin_guiones):
                    messages.error(request, "NIT inválido")
                    return redirect('Clientes')
            else:
                messages.error(request, "Formato de NIT/DPI no válido")
                return redirect('Clientes')

            try:
                form.save()
                messages.success(request, "Cliente guardado con éxito")
            except Exception as e:
                messages.error(request, f"Datos inválidos o ya registrados. ")
                return redirect('Clientes')
        else:
            messages.error(request, "Datos ingresados invalidos o formato incorrecto .")
    
    return redirect('Clientes')


def validar_nit(nit):
    '''Función para validar NIT'''
    nit = nit.replace('-', '').replace(' ', '')  # Elimina guiones y espacios

    if len(nit) < 8 or len(nit) > 10:
        return False  # Longitud no válida para NIT

    try:
        # El último dígito del NIT es el dígito verificador
        digito_verificador = int(nit[-1])
        # Los dígitos restantes son los que se usan para la validación
        numeros = list(map(int, nit[:-1]))

        suma = 0
        multiplicador = 2
        for digito in reversed(numeros):
            suma += digito * multiplicador
            multiplicador = 9 if multiplicador == 2 else 2

        residuo = suma % 11
        digito_calculado = (11 - residuo) % 11

        if digito_calculado == 10:
            digito_calculado = 'K'
        else:
            digito_calculado = str(digito_calculado)

        return digito_calculado == str(digito_verificador)
    except ValueError:
        return False
    

#Validar DPI y NIT
def validar_dpi(dpi):
    dpi = dpi.replace('-', '').replace(' ', '')  # Elimina guiones y espacios

    if len(dpi) != 13:
        return False  # Longitud no válida para DPI

    try:
        # Los primeros 12 dígitos son el número del DPI, el último dígito es el dígito verificador
        digito_verificador = int(dpi[-1])
        numeros = list(map(int, dpi[:-1]))

        suma = 0
        multiplicador = 2
        for digito in reversed(numeros):
            suma += digito * multiplicador
            multiplicador = 1 if multiplicador == 2 else 2

        residuo = suma % 10
        digito_calculado = (10 - residuo) % 10

        return digito_calculado == digito_verificador
    except ValueError:
        return False

def edit_cliente_view(request):
    if request.method == 'POST':
        nit_cui_editar = request.POST.get('id_personal_editar')  
        print(f"NIT/CI recibido: {nit_cui_editar}") 
        if nit_cui_editar:
            try:
                cliente = Cliente.objects.get(pk=nit_cui_editar)
            except Cliente.DoesNotExist:
                messages.error(request, "Cliente no encontrado.")
                return redirect('Clientes')

            # Cargar el formulario con los datos del cliente a editar
            form = EditarClienteForm(request.POST, request.FILES, instance=cliente)

            if form.is_valid():
                # Actualizar los campos del cliente
                estado = request.POST.get('estado_editar') == 'on'
                cliente.estado = estado
                form.save() 
                messages.success(request, "Cliente actualizado con éxito")
            else:
                messages.error(request, "Datos inválidos o ya registrados.")
        else:
            messages.error(request, "ID de cliente inválido.")

    return redirect('Clientes')

def delete_cliente_view(request):
    if request.method == 'POST':
        nit_Cui_cliente = request.POST.get('nit_Cui')
        nuevo_estado = request.POST.get('nuevo_estado')
        print(f"NIT / DPI recibido: {nit_Cui_cliente}")
        print(f"Nuevo estado: {nuevo_estado}")
        print(f"POST data: {request.POST}")
        
        if nit_Cui_cliente and nuevo_estado:
            try:
                cliente = get_object_or_404(Cliente, nit_Cui=nit_Cui_cliente)
                cliente.estado = nuevo_estado
                cliente.save()
                mensaje = f"Cliente {'desactivado' if nuevo_estado == 'inactivo' else 'activado'} con éxito"
                messages.success(request, mensaje)
            except cliente.DoesNotExist:
                messages.error(request, f"No se encontró el Cliente con {nit_Cui_cliente}")
            except Exception as e:
                messages.error(request, f"Error al cambiar el estado del Cliente: {str(e)}")
        else:
            messages.error(request, "No se proporcionaron datos válidos para actualizar el Cliente")
    else:
        messages.error(request, "Método no permitido")
    
    return redirect('Clientes')


#Vistas de Productos

def productos_view(request):
    productos = Producto.objects.all()
    form_producto = AddProductoForm()
    form_editar = EditarProductoForm()
    
    context = {
        'productos': productos,
        'form_producto': form_producto,
        'form_editar': form_editar
    }
    return render(request, 'productos.html', {'productos': productos, 'form_producto': form_producto, 'form_editar': form_editar})

def edit_producto_view(request):
    if request.method == 'POST':
        editarProducto = request.POST.get('id_producto_editar')
        if editarProducto:
            try:
                producto = Producto.objects.get(pk=editarProducto)
                form = EditarProductoForm(request.POST, request.FILES, instance=producto)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Producto actualizado con éxito")
                else:
                    print(form.errors)
                    messages.error(request, "No se pudo actualizar el producto")
            except Producto.DoesNotExist:
                messages.error(request, "Producto no encontrado")
        else:
            messages.error(request, "ID de producto Invalido")
    return redirect('Productos')
            
            

def add_producto_view(request):
    if request.method == 'POST':
        form = AddProductoForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Producto guardado con éxito")
            except:
                messages(request, "Error al guardar el producto")
                return redirect('Productos')
    return redirect('Productos')

def delete_producto_view(request):
    if request.method == 'POST':
        codigo_producto = request.POST.get('codigo')
        nuevo_estado = request.POST.get('nuevo_estado')
        print(f"Codigo recibido: {codigo_producto}")
        print(f"Nuevo estado: {nuevo_estado}")
        print(f"POST data: {request.POST}")
        
        if codigo_producto and nuevo_estado:
            try:
                producto = get_object_or_404(Producto, codigo=codigo_producto)
                producto.estado = nuevo_estado
                producto.save()
                mensaje = f"Producto {'desactivado' if nuevo_estado == 'inactivo' else 'activado'} con éxito"
                messages.success(request, mensaje)
            except producto.DoesNotExist:
                messages.error(request, f"No se encontró el Producto con Código {codigo_producto}")
            except Exception as e:
                messages.error(request, f"Error al cambiar el estado del Producto: {str(e)}")
        else:
            messages.error(request, "No se proporcionaron datos válidos para actualizar el Producto")
    else:
        messages.error(request, "Método no permitido")
    
    return redirect('Productos')



# Vista Venta

class add_ventas(ListView):
    template_name = 'ventas.html'
    model = Egreso

    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request, *args, **kwargs)
    """
    def get_queryset(self):
        return ProductosPreventivo.objects.filter(
            preventivo=self.kwargs['id']
        )
    """
    def post(self, request,*ars, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'autocomplete':
                data = []
                for i in Producto.objects.filter(descripcion__icontains=request.POST["term"])[0:10]:
                    item = i.toJSON()
                    item['value'] = i.descripcion
                    data.append(item)
            else:
                data['error'] = "Ha ocurrido un error"
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data,safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["productos_lista"] = Producto.objects.all()
        context["clientes_lista"] = Cliente.objects.all()
        return context
    
def export_pdf_view(request, id, iva):
    #print(id)
    template = get_template("ticket.html")
    #print(id)
    subtotal = 0 
    iva_suma = 0 

    venta = Egreso.objects.get(pk=float(id))
    datos = ProductosEgreso.objects.filter(egreso=venta)
    for i in datos:
        subtotal = subtotal + float(i.subtotal)
        iva_suma = iva_suma + float(i.iva)

    empresa = "Mi empresa S.A. De C.V"
    context ={
        'num_ticket': id,
        'iva': iva,
        'fecha': venta.fecha_pedido,
        'cliente': venta.cliente.nombre,
        'items': datos, 
        'total': venta.total, 
        'empresa': empresa,
        'comentarios': venta.comentarios,
        'subtotal': subtotal,
        'iva_suma': iva_suma,
    }
    html_template = template.render(context)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; ticket.pdf"
    css_url = os.path.join(settings.BASE_DIR,'index\static\index\css/bootstrap.min.css')
    #HTML(string=html_template).write_pdf(target="ticket.pdf", stylesheets=[CSS(css_url)])
   
    font_config = FontConfiguration()
    HTML(string=html_template, base_url=request.build_absolute_uri()).write_pdf(target=response, font_config=font_config,stylesheets=[CSS(css_url)])

    return response


# Vistas Usuarios

def usuarios_view(request):
    usuarios = Usuario.objects.all()
    form_usuario = AddUsuarioForm()
    form_editar = EditarUsuarioForm()
    
    context = {
        'usuarios': usuarios,
        'form_usuario': form_usuario,
        'usuario_editar': form_editar
    }
    
    return render(request, 'usuarios.html', {'usuarios': usuarios, 'form_usuario': form_usuario, 'form_editar': form_editar})

def add_usuarios_view(request):
    if request.method == 'POST':
        form = AddUsuarioForm(request.POST)
        dpi = request.POST.get('dpi', None)

        # Validación del DPI
        if dpi:
            if not validar_dpi(dpi):
                messages.error(request, "El DPI ingresado no es válido.")
                return redirect('Usuarios')
            
            if Usuario.objects.filter(dpi=dpi).exists():
                messages.error(request, "DPI ingresado ya existe.")
                return redirect('Usuarios')

        # Validación del formulario
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Usuario guardado con éxito.")
            except IntegrityError:
                messages.error(request, "Error: Datos inválidos o ya registrados.")
            except Exception as e:
                messages.error(request, f"Error inesperado: {str(e)}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en {field}: {error}")

    return redirect('Usuarios')

def edit_usuario_view(request):
    if request.method == 'POST':
        dpi_editar = request.POST.get('dpi_usuario_editar')  
        print(f"DPI recibido: {dpi_editar}") 
        
        if dpi_editar:
            try:
                usuario = get_object_or_404(Usuario, dpi=dpi_editar)
            except Usuario.DoesNotExist:
                messages.error(request, "Usuario no encontrado.")
                return redirect('Usuarios')

            # Cargar el formulario con los datos del usuario a editar
            form = EditarUsuarioForm(request.POST, request.FILES, instance=usuario)

            if form.is_valid():
                form.save() 
                messages.success(request, "Usuario actualizado con éxito")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"Error en {field}: {error}")
        else:
            messages.error(request, "DPI de usuario inválido.")

    return redirect('Usuarios')


def toggle_usuario_estado(request):
    if request.method == 'POST':
        dpi_usuario = request.POST.get('dpi')
        nuevo_estado = request.POST.get('nuevo_estado')
        print(f"DPI recibido: {dpi_usuario}")
        print(f"Nuevo estado: {nuevo_estado}")
        print(f"POST data: {request.POST}")
        
        if dpi_usuario and nuevo_estado:
            try:
                usuario = get_object_or_404(Usuario, dpi=dpi_usuario)
                usuario.estado = nuevo_estado
                usuario.save()
                mensaje = f"Usuario {'desactivado' if nuevo_estado == 'inactivo' else 'activado'} con éxito"
                messages.success(request, mensaje)
            except Usuario.DoesNotExist:
                messages.error(request, f"No se encontró el usuario con DPI {dpi_usuario}")
            except Exception as e:
                messages.error(request, f"Error al cambiar el estado del usuario: {str(e)}")
        else:
            messages.error(request, "No se proporcionaron datos válidos para actualizar el usuario")
    else:
        messages.error(request, "Método no permitido")
    
    return redirect('Usuarios')

