# toma y analiza los ultimos codigos de deepseek de el chat nueva appadmin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.urls import reverse
from apps.newapp.models import perfumes, desodorantes, cremas
from apps.appadmin.models import Viaje,Fuentes
from django.contrib.auth import authenticate,login
from apps.appadmin.forms import formviaje
from django.http import HttpResponseRedirect, JsonResponse
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
   
    lista_desodorantes = desodorantes.objects.all().order_by('-id')
    
    # Estadísticas para desodorantes
    total_desodorantes_count = desodorantes.objects.count()
    valor_total_desodorantes = desodorantes.objects.aggregate(total=Sum('precio_inv'))['total'] or 0
    
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

@csrf_exempt  
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

def actualizar_viaje(request, viaje_fecha):
  
    try:
       
        viaje = get_object_or_404(Viaje, fecha=viaje_fecha)
        
        if request.method == 'GET':
            return render(request, 'editar_viaje.html', {
                'viaje': viaje,
                'fecha_actual': viaje.fecha,
                'inversion_actual': viaje.inversion
            })
        
        elif request.method == 'POST':
            nueva_fecha = request.POST.get('fecha')
            nueva_inversion = request.POST.get('inversion')
            
            
            if not nueva_fecha or not nueva_inversion:
                messages.error(request, '❌ Todos los campos son requeridos')
                return render(request, 'editar_viaje.html', {'viaje': viaje})
            
            try:
                
                if nueva_fecha != str(viaje.fecha):
                    if Viaje.objects.filter(fecha=nueva_fecha).exists():
                        messages.error(request, '❌ Ya existe un viaje con esta fecha')
                        return render(request, 'editar_viaje.html', {'viaje': viaje})
                
                
                viaje.fecha = nueva_fecha
                viaje.inversion = float(nueva_inversion)
                viaje.save()
                
                messages.success(request, '✅ Viaje actualizado exitosamente')
                return HttpResponseRedirect(reverse('actualizar_fuente', args=[viaje_fecha]))
                
            except ValueError:
                messages.error(request, '❌ La inversión debe ser un número válido')
                return render(request, 'editar_viaje.html', {'viaje': viaje})
            except Exception as e:
                messages.error(request, f'❌ Error al actualizar: {str(e)}')
                return render(request, 'editar_viaje.html', {'viaje': viaje})
    
    except Viaje.DoesNotExist:
        messages.error(request, '❌ El viaje no existe')
        
    
def actualizar_fuente(request, viaje_fecha):
    try:
        fuentes_filtradas = Fuentes.objects.filter(fechaF=viaje_fecha)
        
        # Crear lista de tuplas (fuente, inversion) - SOLUCIÓN CORRECTA
        fuentes_data = []
        for fuente in fuentes_filtradas:
            fuentes_data.append({
                'fuente': fuente.fuente,
                'inversion': fuente.invertido
            })
        
        if request.method == 'GET':
            return render(request, 'editar_fuentes.html', {
                'fuentes_data': fuentes_data,  # Cambio clave aquí
                'viaje_fecha': viaje_fecha
            })
        
        elif request.method == 'POST':
            nueva_fuentes = request.POST.getlist('fuente[]')
            nueva_inversiones = request.POST.getlist('invertido[]')
            
            if not nueva_fuentes or not nueva_inversiones:
                messages.error(request, '❌ Todos los campos son requeridos')
                return render(request, 'editar_fuentes.html', {
                    'fuentes_data': fuentes_data,
                    'viaje_fecha': viaje_fecha
                })
            
            fuentes_lista = list(fuentes_filtradas)
            
            for i in range(len(fuentes_lista)):
                if i < len(nueva_fuentes):
                    fuentes_lista[i].fuente = nueva_fuentes[i]
                
                if i < len(nueva_inversiones):
                    try:
                        nueva_inversion_float = float(nueva_inversiones[i])
                        fuentes_lista[i].invertido = nueva_inversion_float
                    except ValueError:
                        messages.error(request, f'❌ Error: La inversión debe ser un número válido en la fuente {i+1}')
                        return render(request, 'editar_fuentes.html', {
                            'fuentes_data': fuentes_data,
                            'viaje_fecha': viaje_fecha
                        })
                
                fuentes_lista[i].save()
                
            messages.success(request, '✅ Fuentes actualizadas correctamente')
            return redirect('dashboard') 
            
    except Exception as e:
        messages.error(request, f'❌ Error: {str(e)}')
        return render(request, 'editar_fuentes.html', {
            'fuentes_data': fuentes_data,
            'viaje_fecha': viaje_fecha
        })
       
def agregar_perfume(request):
    if request.method == 'POST':
        try:
        
               
                nombre = request.POST.get('nombre')
                descripcion = request.POST.get('descripcion')
                precio = request.POST.get('precio')
                precio_inv = request.POST.get('precio_inv')
                genero = request.POST.get('genero') 
                tamano = request.POST.get('tamano')
                imagen = request.FILES.get('imagen') 
            
          
                if not nombre or not precio or not genero or not tamano:
                  return JsonResponse({
                    'success': False,
                    'error': 'Faltan campos obligatorios'
                }, status=400)
            
            
                perfume = perfumes.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                precio=float(precio),
                precio_inv=float(precio_inv) if precio_inv else None,
                genero=genero,
                tamano=int(tamano),
                imagen=imagen
            )
                
                return JsonResponse({
                'success': True,
                'message': 'Perfume creado exitosamente',
                
                'nombre': perfume.nombre
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def agregar_desodorante(request):
    if request.method == 'POST':
        try:
           
            id_desodorante = request.POST.get('ID')  # Cambiado de 'id' a 'ID'
            marca = request.POST.get('marca')
            descripcion = request.POST.get('descripcion')
            precio = request.POST.get('precio')
            precio_inv = request.POST.get('precio_inv')
            genero = request.POST.get('genero') 
            tamano = request.POST.get('tamano')
            duracion = request.POST.get('duracion')
            cantidad = request.POST.get('cantidad')
            imagen = request.FILES.get('imagen')
            
            
            if not id_desodorante or not marca or not precio or not genero or not tamano or not duracion:
                return JsonResponse({
                    'success': False,
                    'error': 'Faltan campos obligatorios'
                }, status=400)
            
          
            desodorante = desodorantes.objects.create(  
                id=id_desodorante,
                marca=marca,
                descripcion=descripcion,
                precio=float(precio),
                precio_inv=float(precio_inv) if precio_inv else None,
                genero=genero,
                tamano=int(tamano),
                duracion=int(duracion),
                cantidad=int(cantidad) if cantidad else 0,
                imagen=imagen,
                
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Desodorante creado exitosamente',
                'nombre': desodorante.marca  # Cambiado de id a marca
            })
            
        except Exception as e:
            # Log del error para debugging
            print(f"Error al crear desodorante: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def agregar_crema(request):
    if request.method == 'POST':
        try:
            # Obtener datos - CORREGIDO: nombres de campos
            idcrema = request.POST.get('idcrema')  # Debe coincidir con name="idcrema" en HTML
            marca = request.POST.get('marca')
            descripcion = request.POST.get('descripcion')
            precio = request.POST.get('precio')
            precio_inv = request.POST.get('precio_inv')
            tamano = request.POST.get('tamano')
            cantidad = request.POST.get('cantidad')
            imagen = request.FILES.get('imagen')
            
            # Validar campos obligatorios - CORREGIDO: agregar marca y cantidad
            if not idcrema or not marca or not precio or not tamano:
                return JsonResponse({
                    'success': False,
                    'error': 'Faltan campos obligatorios'
                }, status=400)
            
            # CORREGIDO: El modelo no puede llamarse 'cremas' (es la variable)
            # Debe llamarse 'Crema' o como tengas definido el modelo
            crema = cremas.objects.create(  # Cambiado el nombre del modelo
                idcremas=idcrema,  # Campo ID en el modelo
                marca=marca,  # ¡IMPORTANTE! Falta en tu código original
                descripcion=descripcion,
                precio=float(precio),
                precio_inv=float(precio_inv) if precio_inv else None,
                tamano=int(tamano),
                cantidad=int(cantidad) if cantidad else 0,
                imagen=imagen,
                
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Crema creada exitosamente',  # CORREGIDO: mensaje
                'nombre': crema.marca  # Cambiado de idcremas a marca
            })
            
        except Exception as e:
            # Log del error para debugging
            print(f"Error al crear crema: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def eliminar_perfume(request , nombrep):
    if request.method== 'POST':
        perfume=get_object_or_404(perfumes, nombre=nombrep)
        perfume.delete()
    return redirect('gestionperfumes')  
     
def eliminar_desodorante(request, iddesodo):
    if request.method == 'POST':
        desodorante=get_object_or_404(desodorantes, id= iddesodo)
        desodorante.delete()
        
    return redirect('desodoadmin')    
def eliminar_crema(request,idcremas):
    if request.method == 'POST':
        crema=get_object_or_404(cremas,idcremas=idcremas)
        crema.delete()
    return redirect('cremasadmin')     