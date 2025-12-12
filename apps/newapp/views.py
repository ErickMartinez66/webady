from django.shortcuts import render
from apps.newapp.models import perfumes,cremas,desodorantes


def vistaprin(request):
    return render(request,'principal.html')


def vistaperfumes(request):
    boton_pulsado = request.GET.get('boton',None)
    
    if boton_pulsado == 'todos':
        perfumes_list = perfumes.objects.all()
        context = {
        'perfumes': perfumes_list,
        'titulo': 'Nuestra Colección de Perfumes'
        }
        return render(request, 'perfumes.html', context)
    elif boton_pulsado == 'mujer':
        perfumes_list = perfumes.objects.filter(genero='F')
        context = {
        'perfumes': perfumes_list,
        'titulo': 'Nuestra Colección de Perfumes'
        }
        return render(request, 'perfumes.html', context)
    elif boton_pulsado == 'hombre':
        perfumes_list = perfumes.objects.filter(genero='M')
        context = {
        'perfumes': perfumes_list,
        'titulo': 'Nuestra Colección de Perfumes'
        }
        return render(request, 'perfumes.html', context)
    elif boton_pulsado == 'unisex':
        perfumes_list = perfumes.objects.filter(genero='U')
        context = {
        'perfumes': perfumes_list,
        'titulo': 'Nuestra Colección de Perfumes'
        }
        return render(request, 'perfumes.html', context)
    else:
        perfumes_list = perfumes.objects.all()
        context = {
            'perfumes': perfumes_list,
            'titulo': 'Nuestra Colección de Perfumes'
        }
        return render(request, 'perfumes.html', context)

def vistadesodo(request):
    boton_pulsado = request.GET.get('boton',None)
    
    if boton_pulsado == 'todos':
        desodo_list = desodorantes.objects.all()
        context = {
        'desodorantes': desodo_list,
        'titulo': 'Nuestra Colección de Desodorantes'
        }
        return render(request, 'desodorantes.html', context)
    elif boton_pulsado == 'mujer':
        desodo_list = desodorantes.objects.filter(genero='F')
        context = {
        'desodorantes': desodo_list,
        'titulo': 'Nuestra Colección de Desodorantes'
        }
        return render(request, 'desodorantes.html', context)
    elif boton_pulsado == 'hombre':
        desodo_list = desodorantes.objects.filter(genero='M')
        context = {
        'desodorantes': desodo_list,
        'titulo': 'Nuestra Colección de Desodorantes'
        }
        return render(request, 'desodorantes.html', context)
    elif boton_pulsado == 'unisex':
        desodo_list = desodorantes.objects.filter(genero='U')
        context = {
        'desodorantes': desodo_list,
        'titulo': 'Nuestra Colección de Desodorantes'
        }
        return render(request, 'desodorantes.html', context)
    else:
        desodo_list = desodorantes.objects.all()
        context = {
            'desodorantes': desodo_list,
            'titulo': 'Nuestra Colección de Desodorantes'
        }
        return render(request, 'desodorantes.html', context)

def vistacremas(request):
    cremas_list = cremas.objects.all()
    context = {
        'cremas': cremas_list,
        'titulo': 'Nuestra Colección de cremas'
    }
    return render(request, 'cremas.html', context)

# recuerda hacer los metodos para el filtrado

    
    