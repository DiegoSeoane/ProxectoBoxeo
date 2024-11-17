import re
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import loader
from .models import Competidor,Combate,Evento,Usuario
from django.db.models import Q, Count
from .forms import CompetidorForm, CombateForm, EventoForm, RexistroUsuarioForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

#Variables

NUMERO_LIKES_DESTACADO = 10


def inicioHTML(request):
  template = loader.get_template('index.html')
  listaEventos = Evento.objects.all().values().order_by('-data_evento')[:3]
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
    listaEventos = Evento.objects.all().order_by('-data_evento')
    eventos_con_combates = []

    for evento in listaEventos:
        combates_evento = Combate.objects.filter(evento_combate=evento)
        eventos_con_combates.append({
            'evento': evento,
            'combates': combates_evento
        })

    template = loader.get_template('eventos.html')
    context = {
        'eventos_con_combates': eventos_con_combates,
        'NUMERO_LIKES_DESTACADO':NUMERO_LIKES_DESTACADO
    }
    return HttpResponse(template.render(context, request))


def competidoresHTML(request):

    # Función para extraer o numero do peso
    def peso_numero(weight_str):
      match = re.search(r"(-\d+)$", weight_str)
      return int(match.group(1)) if match else 0


    competidores_por_peso = Competidor.objects.values('peso_competidor').annotate(count=Count('id_competidor')).order_by('peso_competidor')

    # Agrupar competidores por peso
    competidores_agrupados = {}
    for competidor in Competidor.objects.order_by('apelidos_competidor'):
        peso = competidor.peso_competidor
        if peso not in competidores_agrupados:
            competidores_agrupados[peso] = []
        competidores_agrupados[peso].append(competidor)

    competidores_agrupados = dict(sorted(competidores_agrupados.items(), key=lambda item: peso_numero(item[0]), reverse=True))

    for peso, competidores in competidores_agrupados.items():
        competidores.sort(key=lambda competidor: competidor.nome_competidor.lower())

    contido = {
        'competidores_por_peso': competidores_por_peso,
        'competidores_agrupados': competidores_agrupados
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
        
    referer_url = request.META.get('HTTP_REFERER')
    return redirect(referer_url)

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
    # As estadisticas necesitan un numero menor a 1 para que funcione correctamente, por eso non usamos porcentaxe
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
    'porcentaxeEmpates':porcentaxeEmpatesStats,
    'NUMERO_LIKES_DESTACADO':NUMERO_LIKES_DESTACADO
  }
  template = loader.get_template('perfilCompetidor.html')
  return HttpResponse(template.render(contido, request))

def eventoEspecificoHTML(request, id):
  template = loader.get_template('eventoEspecifico.html')
  eventoEspecifico = Evento.objects.get(id_evento = id)
  combates = Combate.objects.filter(evento_combate = eventoEspecifico)

  contido = {
    'combates':combates,
    'evento': eventoEspecifico,
    'NUMERO_LIKES_DESTACADO':NUMERO_LIKES_DESTACADO
  }
  return HttpResponse(template.render(contido, request))
  

def combateHTML(request, id):
  combateEspecifico = Combate.objects.get(id_combate = id)
  esquinaAzul = Competidor.objects.get(id_competidor = combateEspecifico.boxeador_azul.id_competidor)
  esquinaVermella = Competidor.objects.get(id_competidor = combateEspecifico.boxeador_vermello.id_competidor)
  likes = Combate.objects.filter(id_combate = id).values('likes').annotate(count = Count('likes'))
  contido = {
    'combate': combateEspecifico,
    'likes':likes,
    'esquinaAzul':esquinaAzul,
    'esquinaVermella':esquinaVermella,
    'NUMERO_LIKES_DESTACADO':NUMERO_LIKES_DESTACADO
  }
  template = loader.get_template('combate.html')
  return HttpResponse(template.render(contido, request))
  
# Administracion
@login_required
def administracion(request):  
  if not request.user.is_superuser:
    return HttpResponseForbidden(render(request,'403.html'))

  template = loader.get_template('administracion/administrador.html')
  contido = {}
  return HttpResponse(template.render(contido, request))

# Engadir información (CRUD)
@login_required
def engadir(request):
  if not request.user.is_superuser:
    return HttpResponseForbidden("Non tes permisos para acceder a esta páxina.")
  
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

@login_required
def engadir_competidor(request):
  if not request.user.is_superuser:
    return HttpResponseForbidden("Non tes permisos para acceder a esta páxina.")
  tipo = 'Competidor'
  if request.method == "POST":
     form = CompetidorForm(request.POST, request.FILES)
     if form.is_valid():
         form.save()            
         return redirect('engadirCompetidor')
  else:
    form = CompetidorForm()
 
  return render(request, 'administracion/engadir.html', {'form': form, 'tipo':tipo})

@login_required
def engadir_combate(request):
  if not request.user.is_superuser:
    return HttpResponseForbidden("Non tes permisos para acceder a esta páxina.")
  
  tipo = 'Combate'
  if request.method == "POST":
    form = CombateForm(request.POST, request.FILES)
  if form.is_valid():
      form.save()
      return redirect('engadirCombate')
  else:
      form = CombateForm()
    
  return render(request, 'administracion/engadir.html', {'form': form, 'tipo':tipo})

@login_required
def engadir_evento(request):
  if not request.user.is_superuser:
    return HttpResponseForbidden("Non tes permisos para acceder a esta páxina.")
  tipo = 'Evento'        
  if request.method == "POST":
      form = EventoForm(request.POST, request.FILES)
      if form.is_valid():
          form.save()
          return redirect('engadirEvento')
  else:
      form = EventoForm()
  
  return render(request, 'administracion/engadir.html', {'form': form, 'tipo':tipo})


# Modificar información (CRUD)

@login_required
def modificar(request):
  if not request.user.is_superuser:
    return HttpResponseForbidden("Non tes permisos para acceder a esta páxina.")
  
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

@login_required
def modificar_competidor(request,competidor_id):
  if not request.user.is_superuser:
    return HttpResponseForbidden("Non tes permisos para acceder a esta páxina.")
  
  competidor = get_object_or_404(Competidor, id_competidor=competidor_id)
  tipo = 'Competidor'
  if request.method == 'POST':
    form = CompetidorForm(request.POST, request.FILES, instance=competidor)
    if form.is_valid():
      form.save()
      return redirect('modificar')
  else:
    form = CompetidorForm(instance=competidor)
  return render(request, 'administracion/modificarFormulario.html', {'form':form, 'tipo':tipo})

@login_required
def modificar_combate(request,combate_id):
  if not request.user.is_superuser:
    return HttpResponseForbidden("Non tes permisos para acceder a esta páxina.")
  
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

@login_required
def modificar_evento(request,evento_id):
  if not request.user.is_superuser:
    return HttpResponseForbidden("Non tes permisos para acceder a esta páxina.")
  
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
@login_required
def eliminar(request):
  if not request.user.is_superuser:
    return HttpResponseForbidden("Non tes permisos para acceder a esta páxina.")
  
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

@login_required
def eliminarCompetidor(request, competidor_id):
  if not request.user.is_superuser:
    return HttpResponseForbidden("Non tes permisos para acceder a esta páxina.")
  
  competidor = get_object_or_404(Competidor, id_competidor=competidor_id)
  if request.method == 'POST':
      competidor.delete()
      return redirect('eliminar')
  return HttpResponseRedirect(reverse('competidoresPage'))
  
@login_required
def eliminarCombate(request, combate_id):
  if not request.user.is_superuser:
    return HttpResponseForbidden("Non tes permisos para acceder a esta páxina.")
  
  combate = get_object_or_404(Combate, id_combate=combate_id)
  if request.method == 'POST':
      combate.delete()
      return redirect('eliminar')
  return HttpResponseRedirect(reverse('competidoresPage'))

@login_required
def eliminarEvento(request, evento_id):
  if not request.user.is_superuser:
    return HttpResponseForbidden("Non tes permisos para acceder a esta páxina.")
  
  eventos = get_object_or_404(Evento, id_evento =evento_id)
  
  if request.method == 'POST':
      eventos.delete()
      return redirect('eliminar')
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