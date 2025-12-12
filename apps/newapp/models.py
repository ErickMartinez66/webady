

from django.db import models
from django.core.files.base import ContentFile
from PIL import Image
import io
import os
from pathlib import Path

# Tus choices existentes
class TypeChoices(models.TextChoices):
    M = 'M', 'Masculino'
    F = 'F', 'Femenino' 
    U = 'U', 'Unisex'


class perfumes(models.Model):
    nombre = models.CharField(primary_key=True, max_length=50)
    descripcion = models.TextField()
    precio = models.IntegerField()
    precio_inv = models.IntegerField(null=True)
    genero = models.CharField(max_length=1, choices=TypeChoices.choices)
    tamano = models.IntegerField()
    imagen = models.ImageField(upload_to='perfumes/', null=True, blank=True)
    cantidad = models.IntegerField(null=True)
   
    
    def __str__(self):
        return f"{self.nombre} - {self.get_genero_display()} - {self.tamano}ml - ${self.precio}"

class desodorantes(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    marca = models.CharField(max_length=50)
    descripcion = models.TextField()
    precio = models.IntegerField()
    precio_inv = models.IntegerField(null=True)
    genero = models.CharField(max_length=1, choices=TypeChoices.choices)
    tamano = models.IntegerField()
    duracion = models.IntegerField()
    cantidad = models.IntegerField()
    imagen = models.ImageField(upload_to='desodorantes/', null=True, blank=True)
   
    
    def __str__(self):
        return f"{self.marca} - {self.get_genero_display()} - {self.tamano}ml - {self.duracion}h - ${self.precio}"

class cremas(models.Model):
    idcremas = models.CharField(primary_key=True, max_length=50)
    marca = models.CharField(max_length=50)
    descripcion = models.TextField()
    precio = models.IntegerField()
    precio_inv = models.IntegerField(null=True)
    tamano = models.IntegerField()
    cantidad = models.IntegerField()
    imagen = models.ImageField(upload_to='cremas/', null=True, blank=True)
    
  
    def __str__(self):
        return f"{self.marca} - {self.tamano}ml - {self.cantidad}u - ${self.precio}"