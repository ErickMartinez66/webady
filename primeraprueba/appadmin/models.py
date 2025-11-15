from django.db import models

class Viaje(models.Model): 
    fecha = models.DateField(primary_key=True)  
    inversion = models.IntegerField()
    
    def __str__(self):
        return f"Viaje {self.fecha}"

class Fuentes(models.Model): 
    fechaF = models.ForeignKey(Viaje, on_delete=models.CASCADE, related_name='fuentes') 
    fuente = models.CharField(max_length=100)
    invertido = models.IntegerField()
    
    def __str__(self):
        return f"{self.fuente} - {self.fechaF}"