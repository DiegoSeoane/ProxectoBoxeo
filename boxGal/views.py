from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Competidor,Combate,Evento,Usuario
from django.db.models import Q, Count
from .forms import CompetidorForm, CombateForm, EventoForm, RexistroUsuarioForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


def inicioHTML(request):
  template = loader.get_template('index.html')
  listaEventos = Evento.objects.all().values()[:3]
  if request.user.is_authenticated:          
      competidores = request.user.favoritos.all()
  else:        
      competidores = Competidor.objects.annotate(num_seguidores=Count('seguidores')).order_by('-num_seguidores')
  paginator = Paginator(competidores, 5)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  
  contido = {
    'listaEventos':listaEventos,
    'page_obj':page_obj
  }
  return HttpResponse(template.render(contido, request))

def eventosHTML(request):
  listaEventos = Evento.objects.all().values().order_by('-id_evento')
  combates = Combate.objects.all()
  template = loader.get_template('eventos.html')
  contido = {
    'listaEventos':listaEventos,
    'combates':combates
  }
  return HttpResponse(template.render(contido, request))

def competidoresHTML(request):
  listaCompetidores = Competidor.objects.all().values().order_by('-nome_competidor')
  contido = {
    'listaCompetidores':listaCompetidores
  }
  template = loader.get_template('competidores.html')
  return HttpResponse(template.render(contido, request))

@login_required
def alternar_seguir(request, competidor_id):
    competidor = get_object_or_404(Competidor, id_competidor=competidor_id)
    if competidor in request.user.favoritos.all():
        request.user.favoritos.remove(competidor)
    else:
        request.user.favoritos.add(competidor)
    return redirect('competidoresPage')

@login_required
def alternar_like(request, combate_id):
    combate = get_object_or_404(Combate, id_combate=combate_id)
    if combate in request.user.combates_gustados.all():
        request.user.combates_gustados.remove(combate)
    else:
        request.user.combates_gustados.add(combate)
    return redirect(request.META.get('HTTP_REFERER', 'combateEspecifico'), id=combate_id) 

def perfilCompetidorHTML(request, id):
  competidorEspecifico = Competidor.objects.get(id_competidor=id)
  numeroCombates_azul = Combate.objects.filter(boxeador_azul_id=id).count()
  numeroCombates_vermello = Combate.objects.filter(boxeador_vermello_id=id).count()
  listaCombates =  Combate.objects.filter(boxeador_azul=competidorEspecifico) | Combate.objects.filter(boxeador_vermello=competidorEspecifico)

  vitorias= competidorEspecifico.vitorias
  derrotas= competidorEspecifico.derrotas
  empates= competidorEspecifico.empates
  totalCombates = vitorias + derrotas + empates
  if totalCombates > 0:
    # As estadisticas necesitan un numero menor a 1 para que funcione correctamente
    porcentaxeVitoriasStats = (vitorias/totalCombates)
    porcentaxeDerrotasStats = (derrotas/totalCombates)
    porcentaxeEmpatesStats = (empates/totalCombates)
  else:
    porcentaxeVitoriasStats = porcentaxeDerrotasStats = porcentaxeEmpatesStats = 0
  contido = {
    'competidor':competidorEspecifico,
    'totalCombates':totalCombates,
    'numeroCombates_azul':numeroCombates_azul,
    'numeroCombates_vermello':numeroCombates_vermello,
    'listaCombates':listaCombates,
    'vitorias':vitorias,
    'derrotas':derrotas,
    'empates':empates,
    'porcentaxeVitorias':porcentaxeVitoriasStats,
    'porcentaxeDerrotas':porcentaxeDerrotasStats,
    'porcentaxeEmpates':porcentaxeEmpatesStats
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
  contido = {}
  return HttpResponse(template.render(contido, request))

# Engadir información (CRUD)
def engadir(request):
  template = loader.get_template('administracion/engadir.html')
  lista = request.GET.get('','')
  
  contido = {'lista':lista}
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
    tipo = 'Competidor'
    if request.method == "POST":
        form = CompetidorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('competidoresPage')
    else:
        form = CompetidorForm()
    
    return render(request, 'administracion/engadir.html', {'form': form, 'tipo':tipo})

def engadir_combate(request):
    tipo = 'Combate'
    if request.method == "POST":
        form = CombateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('competidoresPage')
    else:
        form = CombateForm()
    
    return render(request, 'administracion/engadir.html', {'form': form, 'tipo':tipo})

def engadir_evento(request):
    tipo = 'Evento'        
    if request.method == "POST":
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('eventosPage')
    else:
        form = EventoForm()
    
    return render(request, 'administracion/engadir.html', {'form': form, 'tipo':tipo})


# Modificar información (CRUD)


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
  tipo = 'Competidor'
  if request.method == 'POST':
    form = CompetidorForm(request.POST, request.FILES, instance=competidor)
    if form.is_valid():
      form.save()
      return redirect('administracion')
  else:
    form = CompetidorForm(instance=competidor)
  return render(request, 'administracion/modificarFormulario.html', {'form':form, 'tipo':tipo})

def modificar_combate(request,combate_id):
  tipo = 'Combate'
  combate = get_object_or_404(Combate, id_combate=combate_id)
  if request.method == 'POST':
    form = CombateForm(request.POST, request.FILES, instance=combate)
    if form.is_valid():
      form.save()
      return redirect('administracion')
  else:
    form = CombateForm(instance=combate)
  return render(request, 'administracion/modificarFormulario.html', {'form':form,'tipo':tipo})

def modificar_evento(request,evento_id):
  tipo = 'Evento'
  evento = get_object_or_404(Evento, id_evento=evento_id)
  if request.method == 'POST':
    form = EventoForm(request.POST, request.FILES, instance=evento)
    if form.is_valid():
      form.save()
      return redirect('administracion')
  else:
    form = EventoForm(instance=evento)
  return render(request, 'administracion/modificarFormulario.html', {'form':form,'tipo':tipo})

# Eliminar información (CRUD)
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
        
        # Autenticamos o usuario
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('indexPage')  # Redirixe á páxina principal
        else:
            messages.error(request, 'Credenciales inválidas')
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})
    
    return render(request, 'login.html')

def logoutPersonalizado(request):
  
    logout(request)
  
    return redirect('indexPage') # Redirixe á páxina principal