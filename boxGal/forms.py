from django import forms
from .models import Combate, Competidor, Evento

class CompetidorForm(forms.ModelForm):
    class Meta:
        model = Competidor
        fields = ['nome_competidor', 'apelidos_competidor', 'foto_competidor', 'peso_competidor', 'vitorias', 'derrotas', 'empates']
        
class CombateForm(forms.ModelForm):
    class Meta:
        model = Combate
        fields = ['boxeador_azul', 'boxeador_vermello', 'evento_combate', 'peso_combate', 'categoria_combate', 'arbitro', 'resultado', 'data_combate']
        
class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nome_evento', 'lugar_evento', 'data_evento', 'foto_evento']