from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static 
from django.urls import path,include
from .views import panel_control,gestion_perfumes,gestion_cremas,gestion_desodorantes,login_user,agregar_viaje




# urls.py
from django.urls import path



urlpatterns = [
    path('entrar/',login_user, name='entrar'),
    path('dashboard/', panel_control, name='dashboard'),
    path('gestionperfumes/', gestion_perfumes, name='gestionperfumes'),
    path('desodoadmin/', gestion_desodorantes, name='desodoadmin'),
    path('cremasadmin/',gestion_cremas, name='cremasadmin'),
    path('agregar_viaje/',agregar_viaje, name='agregar_viaje'),
    
    
    
]