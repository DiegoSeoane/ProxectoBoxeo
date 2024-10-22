from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Competidor,Combate,Evento,Usuario
from django.db.models import Q, Count
from .forms import CompetidorForm, CombateForm, EventoForm, RexistroUsuarioForm
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import logout


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

def combateHTML(request, id):
  combateEspecifico = Combate.objects.get(id_combate = id)
  likes = Combate.objects.filter(id_combate = id).values('likes').annotate(count = Count('likes'))
  contido = {
    'combate': combateEspecifico,
    'likes':likes
  }
  template = loader.get_template('combate.html')
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

# Apartado usuarios

def rexistro_usuario(request):
    if request.method == 'POST':
        form = RexistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            # Non ten likes nin seguimentos por defecto
            usuario.save()
            return redirect('indexPage')
    else:
        form = RexistroUsuarioForm()
    return render(request, 'rexistro.html', {'form': form})

User = get_user_model()


def inicio_sesion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Autenticamos al usuario con el username
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('indexPage')  # Redirige a la página principal
        else:
            messages.error(request, 'Credenciales inválidas')
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})
    
    return render(request, 'login.html')
  
def custom_logout(request):
    logout(request)
    return redirect('indexPage')