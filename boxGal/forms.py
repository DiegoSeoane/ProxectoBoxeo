from django import forms
from .models import Combate, Competidor, Evento, Usuario
from django.contrib.auth.forms import UserCreationForm


class CompetidorForm(forms.ModelForm):
    class Meta:
        model = Competidor
        fields = ['nome_competidor', 'apelidos_competidor', 'foto_competidor', 'peso_competidor', 'vitorias', 'derrotas', 'empates']
        widgets = {
            'nome_competidor': forms.TextInput(attrs={'class': 'form-control'}),
            'apelidos_competidor': forms.TextInput(attrs={'class': 'form-control'}),
            'foto_competidor': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'peso_competidor': forms.NumberInput(attrs={'class': 'form-control'}),
            'vitorias': forms.NumberInput(attrs={'class': 'form-control'}),
            'derrotas': forms.NumberInput(attrs={'class': 'form-control'}),
            'empates': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
class CombateForm(forms.ModelForm):
    class Meta:
        model = Combate
        fields = ['boxeador_azul', 'boxeador_vermello', 'evento_combate', 'peso_combate', 'categoria_combate', 'arbitro', 'resultado', 'data_combate']
        widgets = {
            'boxeador_azul': forms.Select(attrs={'class': 'form-select'}),
            'boxeador_vermello': forms.Select(attrs={'class': 'form-select'}),
            'evento_combate': forms.Select(attrs={'class': 'form-select'}),
            'peso_combate': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria_combate': forms.TextInput(attrs={'class': 'form-control'}),
            'arbitro': forms.TextInput(attrs={'class': 'form-control'}),
            'resultado': forms.TextInput(attrs={'class': 'form-control'}),
            'data_combate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        
class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nome_evento', 'lugar_evento', 'data_evento', 'foto_evento']
        widgets = {
            'nome_evento': forms.TextInput(attrs={'class': 'form-control'}),
            'lugar_evento': forms.TextInput(attrs={'class': 'form-control'}),
            'data_evento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'foto_evento': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        

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