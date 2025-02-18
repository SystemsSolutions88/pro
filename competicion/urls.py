from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_competidores, name='lista_competidores'),
    path('agregar/', views.agregar_competidor, name='agregar_competidor'),
    path('iniciar/<int:pk>/', views.iniciar_carrera, name='iniciar_carrera'),
    path('finalizar/<int:pk>/', views.finalizar_carrera, name='finalizar_carrera'),
    path('resultados/', views.mostrar_resultados, name='mostrar_resultados'),
    path('eliminar_datos/', views.eliminar_datos, name='eliminar_datos'),
    path('iniciar_categoria/<str:categoria>/', views.iniciar_carrera_categoria, name='iniciar_carrera_categoria'),
    path('finalizar_numero/<int:numero_corredor>/', views.finalizar_carrera_por_numero, name='finalizar_carrera_por_numero'),
]

