from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.inicioHTML, name='indexPage'),
    path('login/', views.inicio_sesion, name='login'),
    path('logout/', views.logoutPersonalizado, name='logout'),
    path('rexistro/', views.rexistro_usuario, name='rexistroUsuario'),
    path('eventos/', views.eventosHTML, name='eventosPage'),
    path('competidores/', views.competidoresHTML, name='competidoresPage'),
    path('competidores/<int:id>/', views.perfilCompetidorHTML),
    path('combate/<int:id>/', views.combateHTML, name='combateEspecifico'),
    path('administracion/', views.administracion, name='administracion'),
    path('administracion/engadir', views.engadir, name='engadir'),
    path('administracion/modificar', views.modificar, name='modificar'),
    path('administracion/eliminar', views.eliminar, name='eliminar'),
    path('administracion/modificar/competidor/<int:competidor_id>/', views.modificar_competidor, name='modificar_competidor'),
    path('administracion/modificar/combate/<int:combate_id>/', views.modificar_combate, name='modificar_combate'),
    path('administracion/modificar/evento/<int:evento_id>/', views.modificar_evento, name='modificar_evento'),
    path('eliminar/competidor/<int:competidor_id>/', views.eliminarCompetidor, name='eliminarCompetidor'),
    path('eliminar/combate/<int:combate_id>/', views.eliminarCombate, name='eliminarCombate'),
    path('eliminar/evento/<int:evento_id>/', views.eliminarEvento, name='eliminarEvento'),
    path('engadir/competidor/', views.engadir_competidor, name='engadirCompetidor'),
    path('engadir/combate/', views.engadir_combate, name='engadirCombate'),
    path('engadir/evento/', views.engadir_evento, name='engadirEvento'),
    path('combate/<int:combate_id>/like/', views.alternar_like, name='alternar_like'),
    path('alternar_seguir/<int:competidor_id>/', views.alternar_seguir,
name='alternar_seguir'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Esta ultima linea é necesaria para o uso de media en local