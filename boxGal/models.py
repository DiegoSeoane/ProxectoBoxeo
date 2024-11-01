from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Competidor(models.Model):
    id_competidor = models.BigAutoField(auto_created=True, primary_key=True)
    nome_competidor = models.CharField(max_length=255)
    apelidos_competidor = models.CharField(max_length=255)
    peso_competidor = models.CharField(max_length=255)
    vitorias = models.IntegerField()
    derrotas = models.IntegerField()
    empates = models.IntegerField()
    foto_competidor = models.ImageField(upload_to='competidores/', blank=True, null=True)

    def __str__(self):
        return f"{self.nome_competidor} {self.apelidos_competidor} "

    #Foto de competidor na ruta /media/competidores, campo opcional

class Evento(models.Model):
    id_evento = models.BigAutoField(auto_created=True, primary_key=True)
    nome_evento = models.CharField(max_length=255)
    lugar_evento = models.CharField(max_length=255)
    data_evento = models.DateField()
    foto_evento = models.ImageField(upload_to='eventos/', blank=True, null=True)

    #Foto de evento na ruta /media/eventos, campo opcional

    def __str__(self):
        return self.nome_evento
    
    #Foto de evento na ruta /media/eventos, campo opcional

class Usuario(AbstractUser):
    id_usuario = models.BigAutoField(auto_created=True, primary_key=True)
    favoritos = models.ManyToManyField(Competidor, related_name='seguidores',blank=True)
    fotoperfil = models.ImageField(upload_to='fotos_perfil', blank=True, null=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_set',  #Necesario engadir para evitar erro ao migrar
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_permissions_set',  #Necesario engadir para evitar erro ao migrar
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username

# Necesitamos ter o combate debaixo, xa que precisamos do modelo Usuario creado
class Combate(models.Model):
    id_combate = models.BigAutoField(auto_created=True, primary_key=True)
    boxeador_azul = models.ForeignKey(Competidor, related_name='combates_azul', on_delete=models.CASCADE)
    boxeador_vermello = models.ForeignKey(Competidor, related_name='combates_vermello', on_delete=models.CASCADE)
    evento_combate = models.ForeignKey(Evento, on_delete=models.CASCADE)
    peso_combate = models.CharField(max_length=255)
    categoria_combate = models.CharField(max_length=255)
    arbitro = models.CharField(max_length=255)
    resultado = models.CharField(max_length=255)
    data_combate = models.DateField()
    likes = models.ManyToManyField(Usuario,related_name='combates_gustados', blank=True)
    
    def __str__(self):
        return f"{self.boxeador_azul} vs {self.boxeador_vermello}"
