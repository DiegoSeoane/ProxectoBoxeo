from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Competidor,Combate,Evento,Usuario
from django.db.models import Q  

def inicioHTML(request):
  template = loader.get_template('index.html')
  contido = {
    
  }
  return HttpResponse(template.render(contido, request))

def administracion(request):
  listaEventos = Evento.objects.all().values()
  template = loader.get_template('administrador.html')
  contido = {
    
  }
  return HttpResponse(template.render(contido, request))

def eventosHTML(request):
  listaEventos = Evento.objects.all().values()
  template = loader.get_template('eventos.html')
  contido = {
    'listaEventos':listaEventos
  }
  return HttpResponse(template.render(contido, request))

def competidoresHTML(request):
  listaCompetidores = Competidor.objects.all().values()
  contido = {
    'listaCompetidores':listaCompetidores
  }
  template = loader.get_template('competidores.html')
  return HttpResponse(template.render(contido, request))

def perfilCompetidorHTML(request, id):
  competidorEspecifico = Competidor.objects.get(id_competidor=id)
  numeroCombates_azul = Combate.objects.filter(boxeador_azul_id=id).count()
  numeroCombates_vermello = Combate.objects.filter(boxeador_vermello_id=id).count()
  totalCombates = Combate.objects.filter(Q(boxeador_azul_id=id) | Q(boxeador_vermello_id=id)).count()
  listaCombates = Combate.objects.all()
  contido = {
    'competidor':competidorEspecifico,
    'totalCombates':totalCombates,
    'numeroCombates_azul':numeroCombates_azul,
    'numeroCombates_vermello':numeroCombates_vermello,
    'listaCombates':listaCombates,
  }
  template = loader.get_template('perfilCompetidor.html')
  return HttpResponse(template.render(contido, request))
