from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Competidor, Resultado
from .forms import CompetidorForm
from django.utils import timezone

def agregar_competidor(request):
    if request.method == "POST":
        form = CompetidorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_competidores')
    else:
        form = CompetidorForm()
    return render(request, 'competicion/agregar_competidor.html', {'form': form})

@csrf_exempt
def iniciar_carrera(request, pk):
    if request.method == 'POST':
        competidor = get_object_or_404(Competidor, pk=pk)
        competidor.iniciar_cronometro()
        competidor.save()
        return JsonResponse({'status': 'success', 'message': 'Carrera iniciada'})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

@csrf_exempt
def iniciar_carrera_categoria(request, categoria):
    if request.method == 'POST':
        competidores = Competidor.objects.filter(categoria=categoria)
        for competidor in competidores:
            competidor.iniciar_cronometro()
            competidor.save()
        return JsonResponse({'status': 'success', 'message': f'Carrera categoría {categoria} iniciada'})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

@csrf_exempt
def finalizar_carrera(request, pk):
    if request.method == 'POST':
        competidor = get_object_or_404(Competidor, pk=pk)
        if competidor.tiempo_inicio is not None:  # Asegurarse de que la carrera se haya iniciado
            competidor.detener_cronometro()
            competidor.save()
            tiempo_total = competidor.obtener_tiempo()
            if tiempo_total:
                Resultado.objects.create(
                    competidor=competidor,
                    tiempo_total=tiempo_total,
                    posicion=Resultado.objects.filter(competidor__pista=competidor.pista).count() + 1
                )
            return JsonResponse({'status': 'success', 'message': 'Carrera finalizada'})
        return JsonResponse({'status': 'error', 'message': 'La carrera no ha sido iniciada'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

@csrf_exempt
def finalizar_carrera_por_numero(request, numero_corredor):
    if request.method == 'POST':
        competidor = get_object_or_404(Competidor, numero_corredor=numero_corredor)
        if competidor.tiempo_inicio is not None:  # Asegurarse de que la carrera se haya iniciado
            competidor.detener_cronometro()
            competidor.save()
            tiempo_total = competidor.obtener_tiempo()
            if tiempo_total:
                Resultado.objects.create(
                    competidor=competidor,
                    tiempo_total=tiempo_total,
                    posicion=Resultado.objects.filter(competidor__pista=competidor.pista).count() + 1
                )
            return JsonResponse({'status': 'success', 'message': 'Carrera finalizada'})
        return JsonResponse({'status': 'error', 'message': 'La carrera no ha sido iniciada'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

def lista_competidores(request):
    competidores = Competidor.objects.all().order_by('numero_corredor')
    return render(request, 'competicion/lista_competidores.html', {'competidores': competidores})

def mostrar_resultados(request):
    resultados = Resultado.objects.all().order_by('tiempo_total')
    categorias = Competidor.CATEGORIAS  # Obtener la lista de categorías

    # Filtrar y ordenar resultados por categoría
    resultados_por_categoria = {}
    for categoria in categorias:
        resultados_categoria = resultados.filter(competidor__categoria=categoria[0]).order_by('tiempo_total')
        for idx, resultado in enumerate(resultados_categoria):
            resultado.posicion_categoria = idx + 1  # Asignar posición dentro de la categoría
        resultados_por_categoria[categoria[0]] = resultados_categoria

    return render(request, 'competicion/mostrar_resultados.html', {
        'resultados': resultados,
        'resultados_por_categoria': resultados_por_categoria
    })

@csrf_exempt
def eliminar_datos(request):
    if request.method == 'POST':
        Resultado.objects.all().delete()
        Competidor.objects.all().delete()
        return JsonResponse({'status': 'success', 'message': 'Todos los datos han sido eliminados'})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)
