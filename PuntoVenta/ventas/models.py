from typing import Iterable
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.forms import model_to_dict
from django.utils import timezone
from .utils import generar_usuario

# Create your models here.
class Cliente(models.Model):
    nit_Cui = models.CharField(max_length=20, primary_key=True, unique=True, null=False, blank=False)
    nombre = models.CharField(max_length=200, null=True, blank=True)
    correoElectronico = models.EmailField(max_length=200, null=True, blank=True)
    direccion = models.CharField(max_length=200, null=True, blank=True)
    notas = models.TextField(blank=True, null=True)
    
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'clientes'
        verbose_name_plural = 'clientes'
        
    def __str__(self):
        return self.nombre

    
class Producto(models.Model):
    codigo = models.CharField(primary_key=True ,max_length=100, unique=True, null=False, blank=False)
    cantidad = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    descripcion = models.CharField(max_length=255, unique=True, null=False)
    imagen = models.ImageField(upload_to='productos', null=True, blank=True)
    categoria = models.CharField(max_length=100)
    precio_unitario = models.DecimalField(max_digits=15, decimal_places=2, null=False)
    costo_unitario = models.DecimalField(max_digits=15, decimal_places=2, null=False)
    
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    
    class Meta:
        verbose_name = 'productos'
        verbose_name_plural = 'productos'
        order_with_respect_to = 'descripcion'
        
    def __str__(self):
        return self.descripcion

    

class Egreso(models.Model):
    fecha_pedido = models.DateField(max_length=255)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE , null=True , related_name='cliente')
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    pagado = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    comentarios = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    ticket = models.BooleanField(default=True)
    desglosar = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now_add=True , null=True)

    class Meta:
        verbose_name='egreso'
        verbose_name_plural = 'egresos'
        order_with_respect_to = 'fecha_pedido'
    
    def __str__(self):
        return str(self.id)
   

class ProductosEgreso(models.Model):
    egreso = models.ForeignKey(Egreso, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=20, decimal_places=2 , null=False)
    precio = models.DecimalField(max_digits=20, decimal_places=2 , null=False , default=0)
    subtotal = models.DecimalField(max_digits=20, decimal_places=2 , null=False , default=0)
    iva = models.DecimalField(max_digits=20, decimal_places=2 , null=False , default=0)
    total = models.DecimalField(max_digits=20, decimal_places=2 , null=False , default=0)
    created = models.DateTimeField(auto_now_add=True)
    entregado = models.BooleanField(default=True)
    devolucion = models.BooleanField(default=False)

    class Meta:
        verbose_name='producto egreso'
        verbose_name_plural = 'productos egreso'
        order_with_respect_to = 'created'
    
    def __str__(self):
        return self.producto
    
    def toJSON(self):
        item = model_to_dict(self, exclude=['created'])
        return item
    

# Manager personalizado
class UsuarioManager(BaseUserManager):
    def create_user(self, dpi, correoElectronico, nombre, password=None, **extra_fields):
        if not correoElectronico:
            raise ValueError('El usuario debe tener un correo electrónico')
        correoElectronico = self.normalize_email(correoElectronico)
        user = self.model(dpi=dpi, correoElectronico=correoElectronico, nombre=nombre, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, dpi, correoElectronico, nombre, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(dpi, correoElectronico, nombre, password, **extra_fields)

# Modelo de Usuario
class Usuario(AbstractBaseUser, PermissionsMixin):
    dpi = models.CharField(max_length=20, primary_key=True, unique=True, null=False, blank=False)
    nombre = models.CharField(max_length=200, null=True, blank=True)
    clave = models.CharField(max_length=200, null=True, blank=True, default='defaultpassword')
    correoElectronico = models.EmailField(max_length=200, unique=True, null=False, blank=False)  # Asegurarse que sea único
    notas = models.TextField(blank=True, null=True)
    fecha_ingreso = models.DateTimeField(null=True, blank=True)
    rol = models.CharField(max_length=100)
    
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    # Nuevo campo para el nombre de usuario
    usuario = models.CharField(max_length=200, unique=True, blank=True, null=True)

    USERNAME_FIELD = 'correoElectronico'  # Campo utilizado para iniciar sesión
    REQUIRED_FIELDS = ['dpi', 'nombre']  # Campos obligatorios para crear un superusuario

    objects = UsuarioManager()

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
        
    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        if not self.usuario and self.nombre:
            self.usuario = generar_usuario(self.nombre)
        super().save(*args, **kwargs)

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True


usuarios_activos = Usuario.objects.filter(estado='activo')
