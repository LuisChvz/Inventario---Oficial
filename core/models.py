from __future__ import unicode_literals
from django.contrib import admin
from django.core.validators import MinValueValidator
from django.db import models
import decimal
from django.contrib.auth.models import User
from datetime import date
from multiselectfield import MultiSelectField

class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=256, null=False)

class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=256, null=False)
    categoria = models.ForeignKey(Categoria, on_delete = models.CASCADE)
    empaquetado = models.BooleanField(default=False)
    paquetes = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    unidadPaquete = models.IntegerField(null=True)
    sueltas = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    existencias = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
class Movimiento(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.BooleanField(default=False)
    fecha = models.DateField(auto_now=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    medida = models.BooleanField(default=False)
    cantidad = models.IntegerField(null = False, validators=[MinValueValidator(1)])
    paquetes = models.IntegerField(default = 0, validators=[MinValueValidator(0)])
    unidadesSueltas = models.IntegerField(default = 0, validators=[MinValueValidator(0)])
    unidades = models.IntegerField(default = 0, validators=[MinValueValidator(0)])
    existencias = models.IntegerField(default = 0, validators=[MinValueValidator(0)])
    numero = models.IntegerField(default = 0, validators=[MinValueValidator(0)])
    
    
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Movimiento)

