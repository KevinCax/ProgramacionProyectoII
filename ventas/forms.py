from django import forms
import re
import datetime
from django.utils import timezone
from django.contrib import messages
from .utils import generar_usuario
from .models import Cliente, Producto, Usuario
from django.core.exceptions import ValidationError

class AddClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('nit_Cui', 'nombre', 'correoElectronico', 'direccion', 'notas' , 'estado')
        labels = {
            'nit_Cui': 'Nit o Cui: ',
            'nombre': 'Nombre : ',
            'correoElectronico': 'Correo Electrónico: ',
            'direccion': 'Dirección: ',
            'notas': 'Notas: ',
            'estado': 'Estado: ',
        }
        
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre:
            raise ValidationError("El nombre es obligatorio.")
        palabras = nombre.split()
        if len(palabras) < 2:
            raise ValidationError("El nombre debe constar de al menos dos palabras.")
        if not all(palabra.isalpha() for palabra in palabras):
            raise ValidationError("El nombre solo puede contener letras.")
        return nombre

    def clean_correoElectronico(self):
        correo = self.cleaned_data.get('correoElectronico')
        if not correo:
            raise ValidationError("El correo electrónico es obligatorio.")
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, correo):
            raise ValidationError("El correo electrónico no es válido.")
        return correo
        
        
class EditarClienteForm(forms.ModelForm):
     class Meta:
        model = Cliente
        fields = ('nombre','correoElectronico','direccion','notas')
        labels = {
            'nombre': 'Nombre : ',
            'correoElectronico': 'Correo Electrónico: ',
            'direccion': 'Dirección: ',
            'notas': 'Notas: ',
            
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'type': 'text' , 'id': 'nombre_editar'}),
            'correoElectronico': forms.TextInput(attrs={'id': 'correo_editar'}),
            'direccion': forms.TextInput(attrs={'id': 'direccion_editar'}), 
            'notas': forms.TextInput(attrs={'id': 'notas_editar'}),
        }
        
        
class AddProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('codigo', 'cantidad', 'descripcion', 'categoria', 'precio_unitario', 'costo_unitario', 'imagen')
        labels = {
            'codigo': 'Cód. Producto: ',
            'cantidad': 'Cantidad: ',
            'descripcion': 'Descripción de producto: ',
            'categoria': 'Categoría: ',
            'precio_unitario': 'Precio U. GTQ: ',
            'costo_unitario': 'Costo U. GTQ : ',
            'imagen': 'Imagen :',
        }


class EditarProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('cantidad', 'descripcion', 'categoria', 'precio_unitario','costo_unitario','imagen')
        labels = {
            'cantidad': 'Cantidad: ',
            'descripcion': 'Descripción de producto: ',
            'categoria': 'Categoría: ',
            'precio_unitario': 'Precio U. GTQ: ',
            'costo_unitario': 'Costo U. GTQ : ',
            'imagen': 'Imagen :',
        }
        widgets = {
            'cantidad': forms.NumberInput(attrs={'id': 'cantidad_editar'}),
            'descripcion': forms.TextInput(attrs={'id': 'descripcion_editar'}),
            'categoria': forms.TextInput(attrs={'id': 'categoria_editar'}),
            'precio_unitario': forms.NumberInput(attrs={'id': 'precio_editar'}),
            'costo_unitario': forms.NumberInput(attrs={'id': 'costo_editar'}),
            'imagen': forms.FileInput(attrs={'id': 'imagen_editar'}),
        }
        
class AddUsuarioForm(forms.ModelForm):
    confirmar_clave = forms.CharField(widget=forms.PasswordInput())
    
    ROL_CHOICES = [
        ('Vendedor', 'Vendedor'),
        ('Recepcionista', 'Recepcionista'),
        ('Supervisor', 'Supervisor'),
        ('Administrador', 'Administrador'),
    ]

    rol = forms.ChoiceField(choices=ROL_CHOICES, initial='Vendedor')
    
    class Meta:
        model = Usuario
        fields = ('dpi', 'nombre', 'clave', 'confirmar_clave', 'correoElectronico', 'notas', 'fecha_ingreso', 'rol', 'estado')
        widgets = {
            'clave': forms.PasswordInput(),
            'fecha_ingreso': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        labels = {
            'dpi': 'DPI: ',
            'nombre': 'Nombre: ',
            'clave': 'Contraseña: ',
            'confirmar_clave': 'Confirmar Contraseña: ',
            'correoElectronico': 'Correo Electrónico: ',
            'notas': 'Notas: ',
            'fecha_ingreso': 'Fecha de Ingreso: ',
            'rol': 'Cargo: ',
            'estado': 'Estado: ',
        }
        
    def __init__(self, *args, **kwargs):
        super(AddUsuarioForm, self).__init__(*args, **kwargs)
        # Establece la fecha y hora actual como valor por defecto
        self.fields['fecha_ingreso'].initial = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M')
        
        
    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.usuario = generar_usuario(usuario.nombre)
        if commit:
            usuario.save()
        return usuario
        

    # Validar que el nombre contenga al menos dos palabras
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre:
            raise ValidationError("El nombre es obligatorio.")
        palabras = nombre.split()
        if len(palabras) < 2:
            raise ValidationError("El nombre debe constar de al menos dos palabras.")
        if not all(palabra.isalpha() for palabra in palabras):
            raise ValidationError("El nombre solo puede contener letras.")
        return nombre

    # Validar el formato del correo electrónico
    def clean_correoElectronico(self):
        correo = self.cleaned_data.get('correoElectronico')
        if not correo:
            raise ValidationError("El correo electrónico es obligatorio.")
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, correo):
            raise ValidationError("El correo electrónico no es válido.")
        return correo
    
    def clean_clave(self):
        clave = self.cleaned_data.get('clave')
        if not clave:
            raise ValidationError("La clave es obligatoria.")
        
        if len(clave) < 6 or len(clave) > 13:
            raise ValidationError("La clave debe tener entre 6 y 13 caracteres.")
        
        if ' ' in clave:
            raise ValidationError("La clave no puede contener espacios en blanco.")
        
        if not re.search(r'\d', clave):
            raise ValidationError("La clave debe contener al menos un número.")
        
        if not re.search(r'[a-z]', clave):
            raise ValidationError("La clave debe contener al menos una letra minúscula.")
        
        if not re.search(r'[A-Z]', clave):
            raise ValidationError("La clave debe contener al menos una letra mayúscula.")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', clave):
            raise ValidationError("La clave debe contener al menos un carácter especial.")
        
        return clave
    
    def clean_fecha_ingreso(self):
        fecha_ingreso = self.cleaned_data.get('fecha_ingreso')
        if fecha_ingreso:
            # Asegúrate de que fecha_ingreso sea aware
            if timezone.is_naive(fecha_ingreso):
                fecha_ingreso = timezone.make_aware(fecha_ingreso)

            # Compara con la fecha y hora actual
            if fecha_ingreso > timezone.now():
                raise ValidationError("La fecha de ingreso no puede ser en el futuro.")
        return fecha_ingreso

    # Validar que las contraseñas coincidan
    def clean(self):
        cleaned_data = super().clean()
        clave = cleaned_data.get('clave')
        confirmar_clave = cleaned_data.get('confirmar_clave')
        
        if clave and confirmar_clave and clave != confirmar_clave:
            raise ValidationError("Las contraseñas no coinciden.")

    # Método para mostrar alertas
    def handle_validation_errors(self):
        if self.errors:
            for field, errors in self.errors.items():
                for error in errors:
                    messages.error(self.request, error) 
        
class EditarUsuarioForm(forms.ModelForm):
    ROL_CHOICES = [
        ('Vendedor', 'Vendedor'),
        ('Recepcionista', 'Recepcionista'),
        ('Supervisor', 'Supervisor'),
        ('Administrador', 'Administrador'),
    ]

    rol = forms.ChoiceField(
        choices=ROL_CHOICES, 
        initial='Vendedor',
        widget=forms.Select(attrs={'id': 'rol_editar', 'class': 'form-control'})
    )
    
    class Meta:
        model = Usuario
        fields = ('nombre', 'correoElectronico', 'rol', 'notas')
        labels = {
            'nombre': 'Nombre:',
            'correoElectronico': 'Correo Electrónico:',
            'rol': 'Cargo:',
            'notas': 'Notas:',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'type': 'text', 'id': 'nombre_editar', 'class': 'form-control'}),
            'correoElectronico': forms.EmailInput(attrs={'id': 'correo_editar', 'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'id': 'notas_editar', 'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if 'class' not in self.fields[field].widget.attrs:
                self.fields[field].widget.attrs.update({'class': 'form-control'})
