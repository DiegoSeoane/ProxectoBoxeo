from django.contrib import admin
from .models import Usuario, Evento, Competidor, Combate

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Evento)
admin.site.register(Competidor)
admin.site.register(Combate)