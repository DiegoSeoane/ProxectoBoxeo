from django import forms
from .models import Combate, Competidor, Evento, Usuario
from django.contrib.auth.forms import UserCreationForm


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
        
class RexistroUsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'fotoperfil', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super(RexistroUsuarioForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['fotoperfil'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
