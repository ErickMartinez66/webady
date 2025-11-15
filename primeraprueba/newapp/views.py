from django.shortcuts import render
from .models import perfumes,cremas,desodorantes


def vistaprin(request):
    return render(request,'principal.html')


def vistaperfumes(request):
    perfumes_list = perfumes.objects.all()
    context = {
        'perfumes': perfumes_list,
        'titulo': 'Nuestra Colección de Perfumes'
    }
    return render(request, 'perfumes.html', context)

def vistadesodo(request):
    desodo_list = desodorantes.objects.all()
    context = {
        'desodorantes': desodo_list,
        'titulo': 'Nuestra Colección de desodorantes'
    }
    return render(request, 'desodorantes.html', context)

def vistacremas(request):
    cremas_list = cremas.objects.all()
    context = {
        'cremas': cremas_list,
        'titulo': 'Nuestra Colección de cremas'
    }
    return render(request, 'cremas.html', context)

