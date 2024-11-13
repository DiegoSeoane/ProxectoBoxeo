from django import forms
from .models import Combate, Competidor, Evento, Usuario
from django.contrib.auth.forms import UserCreationForm


# Establecemos os pesos que se van usar en diferentes clases
PESO_CHOICES = [
        ('Junior - Masculino', [
            ('Junior M -46 kg', 'Junior M -46 kg'),
            ('Junior M -48 kg', 'Junior M -48 kg'),
            ('Junior M -50 kg', 'Junior M -50 kg'),
            ('Junior M -52 kg', 'Junior M -52 kg'),
            ('Junior M -54 kg', 'Junior M -54 kg'),
            ('Junior M -57 kg', 'Junior M -57 kg'),
            ('Junior M -60 kg', 'Junior M -60 kg'),
            ('Junior M -63 kg', 'Junior M -63 kg'),
            ('Junior M -66 kg', 'Junior M -66 kg'),
            ('Junior M -70 kg', 'Junior M -70 kg'),
            ('Junior M -75 kg', 'Junior M -75 kg'),
            ('Junior M -80 kg', 'Junior M -80 kg'),
            ('Junior M +80 kg', 'Junior M +80 kg'),
        ]),
        ('Junior - Femenino', [
            ('Junior F -46 kg', 'Junior F -46 kg'),
            ('Junior F -48 kg', 'Junior F -48 kg'),
            ('Junior F -50 kg', 'Junior F -50 kg'),
            ('Junior F -52 kg', 'Junior F -52 kg'),
            ('Junior F -54 kg', 'Junior F -54 kg'),
            ('Junior F -57 kg', 'Junior F -57 kg'),
            ('Junior F -60 kg', 'Junior F -60 kg'),
            ('Junior F -63 kg', 'Junior F -63 kg'),
            ('Junior F -66 kg', 'Junior F -66 kg'),
            ('Junior F -70 kg', 'Junior F -70 kg'),
            ('Junior F -75 kg', 'Junior F -75 kg'),
            ('Junior F -80 kg', 'Junior F -80 kg'),
            ('Junior F +80 kg', 'Junior F +80 kg'),
        ]),
        ('Joven - Masculino', [
            ('Joven M -48 kg', 'Joven M -48 kg'),
            ('Joven M -51 kg', 'Joven M -51 kg'),
            ('Joven M -54 kg', 'Joven M -54 kg'),
            ('Joven M -57 kg', 'Joven M -57 kg'),
            ('Joven M -60 kg', 'Joven M -60 kg'),
            ('Joven M -63 kg', 'Joven M -63 kg'),
            ('Joven M -67 kg', 'Joven M -67 kg'),
            ('Joven M -71 kg', 'Joven M -71 kg'),
            ('Joven M -75 kg', 'Joven M -75 kg'),
            ('Joven M -80 kg', 'Joven M -80 kg'),
            ('Joven M -86 kg', 'Joven M -86 kg'),
            ('Joven M -92 kg', 'Joven M -92 kg'),
            ('Joven M +92 kg', 'Joven M +92 kg'),
        ]),
        ('Joven - Femenino', [
            ('Joven F -48 kg', 'Joven F -48 kg'),
            ('Joven F -50 kg', 'Joven F -50 kg'),
            ('Joven F -52 kg', 'Joven F -52 kg'),
            ('Joven F -54 kg', 'Joven F -54 kg'),
            ('Joven F -57 kg', 'Joven F -57 kg'),
            ('Joven F -60 kg', 'Joven F -60 kg'),
            ('Joven F -63 kg', 'Joven F -63 kg'),
            ('Joven F -66 kg', 'Joven F -66 kg'),
            ('Joven F -70 kg', 'Joven F -70 kg'),
            ('Joven F -75 kg', 'Joven F -75 kg'),
            ('Joven F -81 kg', 'Joven F -81 kg'),
            ('Joven F +81 kg', 'Joven F +81 kg'),
        ]),
        ('Élite - Masculino', [
            ('Élite M -48 kg', 'Élite M -48 kg'),
            ('Élite M -51 kg', 'Élite M -51 kg'),
            ('Élite M -54 kg', 'Élite M -54 kg'),
            ('Élite M -57 kg', 'Élite M -57 kg'),
            ('Élite M -60 kg', 'Élite M -60 kg'),
            ('Élite M -63 kg', 'Élite M -63 kg'),
            ('Élite M -67 kg', 'Élite M -67 kg'),
            ('Élite M -71 kg', 'Élite M -71 kg'),
            ('Élite M -75 kg', 'Élite M -75 kg'),
            ('Élite M -80 kg', 'Élite M -80 kg'),
            ('Élite M -86 kg', 'Élite M -86 kg'),
            ('Élite M -92 kg', 'Élite M -92 kg'),
            ('Élite M +92 kg', 'Élite M +92 kg'),
        ]),
        ('Élite - Femenino', [
            ('Élite F -48 kg', 'Élite F -48 kg'),
            ('Élite F -50 kg', 'Élite F -50 kg'),
            ('Élite F -52 kg', 'Élite F -52 kg'),
            ('Élite F -54 kg', 'Élite F -54 kg'),
            ('Élite F -57 kg', 'Élite F -57 kg'),
            ('Élite F -60 kg', 'Élite F -60 kg'),
            ('Élite F -63 kg', 'Élite F -63 kg'),
            ('Élite F -66 kg', 'Élite F -66 kg'),
            ('Élite F -70 kg', 'Élite F -70 kg'),
            ('Élite F -75 kg', 'Élite F -75 kg'),
            ('Élite F -81 kg', 'Élite F -81 kg'),
            ('Élite F +81 kg', 'Élite F +81 kg'),
        ]),
    ]

#Formularios

class CompetidorForm(forms.ModelForm):
    peso_competidor = forms.ChoiceField(
        choices=PESO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Peso"
    )
    class Meta:
        model = Competidor
        fields = ['nome_competidor', 'apelidos_competidor', 'foto_competidor', 'peso_competidor', 'vitorias', 'derrotas', 'empates']
        widgets = {
            'nome_competidor': forms.TextInput(attrs={'class': 'form-control'}),
            'apelidos_competidor': forms.TextInput(attrs={'class': 'form-control'}),
            'foto_competidor': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'vitorias': forms.NumberInput(attrs={'class': 'form-control'}),
            'derrotas': forms.NumberInput(attrs={'class': 'form-control'}),
            'empates': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
class CombateForm(forms.ModelForm):
    RESULTADOS_CHOICES = [
        ('VERMELLA', 'Esquina Vermella'),
        ('AZUL', 'Esquina Azul'),
        ('EMPATE', 'Empate'),
        ('POR DETERMINAR', 'Por determinar')
    ]
    
    resultado = forms.ChoiceField(
        choices=RESULTADOS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Resultado"
    )

    peso_combate = forms.ChoiceField(
        choices=PESO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Peso"
    )
    
    CATEGORIA_CHOICES = [
        ('Junior Masculino', 'Junior Masculino'),
        ('Junior Femenino', 'Junior Femenino'),
        ('Joven Masculino', 'Joven Masculino'),
        ('Joven Femenino', 'Joven Femenino'),
        ('Élite Masculino', 'Élite Masculino'),
        ('Élite Femenino', 'Élite Femenino'),
    ]
    
    categoria_combate = forms.ChoiceField(
        choices= CATEGORIA_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Categoría"    
    )
    
    class Meta:
        model = Combate
        fields = [
            'boxeador_azul', 'boxeador_vermello', 'evento_combate',
            'peso_combate', 'categoria_combate', 'arbitro', 'resultado', 'data_combate'
        ]
        widgets = {
            'boxeador_azul': forms.Select(attrs={'class': 'form-select'}),
            'boxeador_vermello': forms.Select(attrs={'class': 'form-select'}),
            'evento_combate': forms.Select(attrs={'class': 'form-select'}),
            'arbitro': forms.TextInput(attrs={'class': 'form-control'}),
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