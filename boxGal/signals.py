# signals.py
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Combate, Competidor

@receiver(post_save, sender=Combate)
def actualizar_estadisticas(sender, instance, created, **kwargs):
    
    if created:    
        competidor_azul = instance.boxeador_azul
        competidor_vermello = instance.boxeador_vermello
        
        if instance.resultado == 'AZUL':
            competidor_azul.vitorias += 1
            competidor_vermello.derrotas += 1
        elif instance.resultado == 'VERMELLA':
            competidor_vermello.vitorias += 1
            competidor_azul.derrotas += 1
        elif instance.resultado == 'EMPATE':            
            competidor_azul.empates += 1
            competidor_vermello.empates += 1

        competidor_azul.save()
        competidor_vermello.save()
        
@receiver(pre_delete, sender=Combate)
def revertir_estadisticas(sender, instance, **kwargs):
    competidor_azul = instance.boxeador_azul
    competidor_vermello = instance.boxeador_vermello
    # Usamos max(x - 1, 0) para que non existan valores negativos
    if instance.resultado == 'AZUL':
        competidor_azul.vitorias = max(competidor_azul.vitorias - 1, 0)
        competidor_vermello.derrotas = max(competidor_vermello.derrotas - 1, 0)
    elif instance.resultado == 'VERMELLA':
        competidor_vermello.vitorias = max(competidor_vermello.vitorias - 1, 0)
        competidor_azul.derrotas = max(competidor_azul.derrotas - 1, 0)
    elif instance.resultado == 'EMPATE':
        competidor_azul.empates = max(competidor_azul.empates - 1, 0)
        competidor_vermello.empates = max(competidor_vermello.empates - 1, 0)
        
    competidor_azul.save()
    competidor_vermello.save()