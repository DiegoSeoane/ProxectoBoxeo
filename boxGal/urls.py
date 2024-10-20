from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.inicioHTML, name='indexPage'),
    path('eventos/', views.eventosHTML, name='eventosPage'),
    path('competidores/', views.competidoresHTML, name='competidoresPage'),
    path('competidores/<int:id>/', views.perfilCompetidorHTML),
    path('administracion/', views.administracion, name='administracion'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)