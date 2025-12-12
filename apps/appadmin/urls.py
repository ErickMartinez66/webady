from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static 
from django.urls import path,include
from .views import panel_control,gestion_perfumes,gestion_cremas,gestion_desodorantes,actualizar_viaje,eliminar_viaje,login_user,agregar_viaje,agregar_fuente,actualizar_fuente,agregar_perfume,agregar_desodorante,agregar_crema,eliminar_perfume,eliminar_desodorante,eliminar_crema,obtener_perfume,editar_perfume,obtener_crema,editar_crema,obtener_desodorante,editar_desodorante



# urls.py
from django.urls import path



urlpatterns = [
    path('entrar/',login_user, name='entrar'),
    path('dashboard/', panel_control, name='dashboard'),
    path('gestionperfumes/', gestion_perfumes, name='gestionperfumes'),
    path('desodoadmin/', gestion_desodorantes, name='desodoadmin'),
    path('cremasadmin/',gestion_cremas, name='cremasadmin'),
    path('agregar_viaje/',agregar_viaje, name='agregar_viaje'),
    path('agregar_fuente/',agregar_fuente, name='agregar_fuente'),
    path('eliminar_viaje/<str:viaje_fecha>/',eliminar_viaje, name='eliminar_viaje'),
    path('eliminar_perfume/<str:nombrep>/',eliminar_perfume, name='eliminar_perfume'),
    path('eliminar_desodorante/<str:iddesodo>/',eliminar_desodorante, name='eliminar_desodorante'),
    path('eliminar_crema/<str:idcremas>/',eliminar_crema, name='eliminar_crema'),
    path('actualizar_viaje/<str:viaje_fecha>/',actualizar_viaje, name='actualizar_viaje'), 
    path('actualizar_fuente/<str:viaje_fecha>/',actualizar_fuente, name='actualizar_fuente'),
    path('agregar_perfume/',agregar_perfume, name='agregar_perfume'),
    path('agregar_desodorante/',agregar_desodorante, name='agregar_desodorante'),
    path('agregar_crema',agregar_crema, name='agregar_crema'),
    path('obtener-perfume/<str:nombre>/', obtener_perfume, name='obtener_perfume'),
    path('editar-perfume/<str:nombre>/', editar_perfume, name='editar_perfume'),
    path('obtener-crema/<str:id>/', obtener_crema, name='obtener_crema'),
    path('editar-crema/<str:id>/', editar_crema, name='editar_crema'),
    path('obtener-desodorante/<str:id>/', obtener_desodorante, name='obtener_desodorante'),
    path('editar-desodorante/<str:id>/', editar_desodorante, name='editar_desodorante'),
]