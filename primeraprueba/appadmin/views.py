# toma y analiza los ultimos codigos de deepseek de el chat nueva appadmin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Sum, Count, Q
from newapp.models import perfumes, desodorantes, cremas
from .models import Viaje,Fuentes
from django.contrib.auth import authenticate,login
from .forms import formviaje
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def login_user(request):
  
    
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirige a la página que intentaba acceder o al dashboard
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            return render(request, 'entrar.html', {'error': 'Credenciales inválidas'})
    
    return render(request, 'entrar.html')

# Proteger el dashboard
@login_required
def panel_control(request):
    """Vista principal del panel de administración"""
    
    
    total_perfumes_count = perfumes.objects.count()
    total_desodorantes_count = desodorantes.objects.count()
    total_cremas_count = cremas.objects.count()
    total_productos = total_perfumes_count + total_desodorantes_count + total_cremas_count
    
    valor_perfumes_inv = perfumes.objects.aggregate(total=Sum('precio_inv'))['total'] or 0
    valor_desodorantes_inv = desodorantes.objects.aggregate(total=Sum('precio_inv'))['total'] or 0
    valor_cremas_inv = cremas.objects.aggregate(total=Sum('precio_inv'))['total'] or 0
    invertido_total = valor_perfumes_inv + valor_desodorantes_inv +  valor_cremas_inv
    
    valor_perfumes = perfumes.objects.aggregate(total=Sum('precio'))['total'] or 0
    valor_desodorantes = desodorantes.objects.aggregate(total=Sum('precio'))['total'] or 0
    valor_cremas = cremas.objects.aggregate(total=Sum('precio'))['total'] or 0
    valor_total_inventario = valor_perfumes + valor_desodorantes + valor_cremas
    
    ganancia_neta= valor_total_inventario - invertido_total
    
   
    lista_perfumes = perfumes.objects.all().order_by('nombre')
    lista_desodorantes = desodorantes.objects.all().order_by('-id')
    lista_cremas = cremas.objects.all().order_by('-idcremas')
    
    #esto es lo nuevo que hice de los viajes , pq en el html debn haber tablas para cada viaje 
    lista_viajes =Viaje.objects.all().order_by('fecha')
    lista_fuentes =Fuentes.objects.all().order_by('fechaF')
    
    
    context = {
        'total_productos': total_productos,
        'total_perfumes': total_perfumes_count,
        'total_desodorantes': total_desodorantes_count,
        'total_cremas': total_cremas_count,
        
        'ganancia_neta':ganancia_neta,
        'total_invertido': invertido_total ,
        
        'valor_total_inventario': valor_total_inventario,
        'valor_perfumes': valor_perfumes,
        'valor_desodorantes': valor_desodorantes,
        'valor_cremas': valor_cremas,
        
        
        'perfumes': lista_perfumes,
        'desodorantes': lista_desodorantes,
        'cremas': lista_cremas,
        
        'viajes':lista_viajes,
        'fuentes':lista_fuentes,
    }
    
    return render(request, 'dashboard.html', context)

@login_required
def gestion_perfumes(request):
    """Vista específica para gestión de perfumes"""
   
    lista_perfumes = perfumes.objects.all().order_by('nombre')
    
    
    total_perfumes_count = perfumes.objects.count()
    valor_total_perfumes = perfumes.objects.aggregate(total=Sum('precio'))['total'] or 0
    valor_invertido_total=perfumes.objects.aggregate(total=Sum('precio_inv'))['total'] or 0
    ganancia =valor_total_perfumes - valor_invertido_total
    
    context = {
        'perfumes': lista_perfumes,
        'total_perfumes': total_perfumes_count,
        'valor_invertido_perfumes': valor_invertido_total,
        'ganancia_perfumes':ganancia,
        'valor_total_perfumes': valor_total_perfumes,
        'perfumes_activos': total_perfumes_count,
    }
    
    return render(request, 'gestion_perfumes.html', context)

@login_required
def gestion_desodorantes(request):
    """Vista para gestión de desodorantes"""
    # ✅ CORREGIDO: Usar nombre diferente
    lista_desodorantes = desodorantes.objects.all().order_by('-id')
    
    # Estadísticas para desodorantes
    total_desodorantes_count = desodorantes.objects.count()
    valor_total_desodorantes = desodorantes.objects.aggregate(total=Sum('precio'))['total'] or 0
    
    context = {
        'desodorantes': lista_desodorantes,
        'total_desodorantes': total_desodorantes_count,
        'stock_bajo_desodorantes': 0,
        'valor_total_desodorantes': valor_total_desodorantes,
        'desodorantes_activos': total_desodorantes_count,
    }
    
    return render(request, 'gestion_desodorantes.html', context)

@login_required
def gestion_cremas(request):
    """Vista para gestión de cremas"""
    
    lista_cremas = cremas.objects.all().order_by('-idcremas')
    
    
    total_cremas_count = cremas.objects.count()
    valor_total_cremas = cremas.objects.aggregate(total=Sum('precio'))['total'] or 0
    
    context = {
        'cremas': lista_cremas,
        'total_cremas': total_cremas_count,
        'stock_bajo_cremas': 0,
        'valor_total_cremas': valor_total_cremas,
        'cremas_activas': total_cremas_count,
    }
    
    return render(request, 'gestion_cremas.html', context)



def agregar_viaje(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        fecha = data.get('fecha')
        inversion = data.get('inversion')

        if fecha and inversion:
            viaje = Viaje.objects.create(fecha=fecha, inversion=inversion)
            return JsonResponse({'message': 'Viaje creado exitosamente', 'viaje': {'fecha': viaje.fecha, 'inversion': viaje.inversion}})
        else:
            return JsonResponse({'error': 'Datos inválidos'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405),fecha
        
def agregar_fuente(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ultimoviaje = Viaje.objects.last()
        fechaF = ultimoviaje
        fuente =data.get('fuente')
        invertido= data.get('invertido')

        if fechaF and invertido:
            fuente = Fuentes.objects.create(fechaF=fechaF,fuente=fuente,invertido=invertido)
            return JsonResponse({'message': 'fuente creada exitosamente'})
             
        else:
            return JsonResponse({'error': 'Datos inválidos'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)
    

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

@csrf_exempt  # O maneja el CSRF token apropiadamente
def eliminar_viaje(request, viaje_fecha):
    if request.method == 'POST':  
        try:
            viaje = get_object_or_404(Viaje, fecha=viaje_fecha)
            fecha_viaje = viaje.fecha
            
            viaje.delete()
            
           
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error al eliminar: {str(e)}'
            }, status=500)
    
    return redirect('dashboard')