from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Competidor,Combate,Evento,Usuario
from django.db.models import Q
from .forms import CompetidorForm, CombateForm, EventoForm
from django.urls import reverse

def inicioHTML(request):
  template = loader.get_template('index.html')
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

# Administracion

def administracion(request):  
  template = loader.get_template('administracion/administrador.html')
  contido = {
    
  }
  return HttpResponse(template.render(contido, request))



# Engadir 
def engadir(request):
  template = loader.get_template('administracion/engadir.html')
  lista = request.GET.get('lista','competidores')
  
  contido = {}
  if lista == 'competidores':
    contido['lista'] = Competidor.objects.all(),
    contido['tipo'] = 'competidores'
  
  elif lista == 'combates':
    contido['lista'] = Combate.objects.all(),
    contido['tipo'] = 'combates'
  
  elif lista == 'eventos':
    contido['lista'] = Evento.objects.all(),
    contido['tipo'] = 'eventos'
  
  return HttpResponse(template.render(contido, request))

def engadir_competidor(request):
    if request.method == "POST":
        form = CompetidorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('competidoresPage')
    else:
        form = CompetidorForm()
    
    return render(request, 'administracion/engadirCompetidor.html', {'form': form})

def engadir_combate(request):
    if request.method == "POST":
        form = CombateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('competidoresPage')
    else:
        form = CombateForm()
    
    return render(request, 'administracion/engadirCombate.html', {'form': form})

def engadir_evento(request):
    if request.method == "POST":
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('eventosPage')
    else:
        form = EventoForm()
    
    return render(request, 'administracion/engadirCompetidor.html', {'form': form})


def modificar(request):
  template = loader.get_template('administracion/modificar.html')
  lista = request.GET.get('lista','competidores')
  
  contido = {}
  if lista == 'competidores':
    contido['lista'] = Competidor.objects.all(),
    contido['tipo'] = 'competidores'
  
  elif lista == 'combates':
    contido['lista'] = Combate.objects.all(),
    contido['tipo'] = 'combates'
  
  elif lista == 'eventos':
    contido['lista'] = Evento.objects.all(),
    contido['tipo'] = 'eventos'
  
  return HttpResponse(template.render(contido, request))

# Modificar

def modificar(request):
  template = loader.get_template('administracion/modificar.html')
  lista = request.GET.get('lista','competidores')
  
  contido = {}
  if lista == 'competidores':
    contido['lista'] = Competidor.objects.all(),
    contido['tipo'] = 'competidores'
  
  elif lista == 'combates':
    contido['lista'] = Combate.objects.all(),
    contido['tipo'] = 'combates'
  
  elif lista == 'eventos':
    contido['lista'] = Evento.objects.all(),
    contido['tipo'] = 'eventos'
  
  return HttpResponse(template.render(contido, request))

def modificar_competidor(request,competidor_id):
  competidor = get_object_or_404(Competidor, id_competidor=competidor_id)
  if request.method == 'POST':
    form = CompetidorForm(request.POST, request.FILES, instance=competidor)
    if form.is_valid():
      form.save()
      return redirect('administracion')
  else:
    form = CompetidorForm(instance=competidor)
  return render(request, 'administracion/modificarCompetidor.html', {'form':form})

def modificar_combate(request,combate_id):
  combate = get_object_or_404(Combate, id_combate=combate_id)
  if request.method == 'POST':
    form = CombateForm(request.POST, request.FILES, instance=combate)
    if form.is_valid():
      form.save()
      return redirect('administracion')
  else:
    form = CombateForm(instance=combate)
  return render(request, 'administracion/modificarCombate.html', {'form':form})

def modificar_evento(request,evento_id):
  evento = get_object_or_404(Evento, id_evento=evento_id)
  if request.method == 'POST':
    form = EventoForm(request.POST, request.FILES, instance=evento)
    if form.is_valid():
      form.save()
      return redirect('administracion')
  else:
    form = EventoForm(instance=evento)
  return render(request, 'administracion/modificarEvento.html', {'form':form})

# Eliminar
def eliminar(request):
  template = loader.get_template('administracion/eliminar.html')
  lista = request.GET.get('lista','competidores')
  
  contido = {}
  if lista == 'competidores':
    contido['lista'] = Competidor.objects.all(),
    contido['tipo'] = 'competidores'
  
  elif lista == 'combates':
    contido['lista'] = Combate.objects.all(),
    contido['tipo'] = 'combates'
  
  elif lista == 'eventos':
    contido['lista'] = Evento.objects.all(),
    contido['tipo'] = 'eventos'
  
  return HttpResponse(template.render(contido, request))

def eliminarCompetidor(request, competidor_id):
    competidor = get_object_or_404(Competidor, id_competidor=competidor_id)

    if request.method == 'POST':
        competidor.delete()
        return redirect('administracion')

    return HttpResponseRedirect(reverse('competidoresPage'))
  
def eliminarCombate(request, combate_id):
    combate = get_object_or_404(Combate, id_combate=combate_id)

    if request.method == 'POST':
        combate.delete()
        return redirect('administracion')

    return HttpResponseRedirect(reverse('competidoresPage'))
def eliminarEvento(request, evento_id):
    eventos = get_object_or_404(Evento, id_evento =evento_id)

    if request.method == 'POST':
        eventos.delete()
        return redirect('administracion')

    return HttpResponseRedirect(reverse('competidoresPage'))