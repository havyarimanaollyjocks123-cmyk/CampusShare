from django.urls import path
from . import views

urlpatterns = [
    path('depot/', views.depot_ressource, name='depot_ressource'),
    path('mes-depots/', views.mes_depots, name='mes_depots'),

    # Mes nouvelles routes pur la moderation

    path('moderation/', views.file_attente, name='file_attente'),
    path('moderation/<int:ressource_id>/<str:action>/', views.action_moderation, name='action_moderation'),
    path('', views.catalogue, name='catalogue'), # La page principale
    path('telecharger/<int:ressource_id>/', views.telecharger_ressource, name='telecharger_ressource'),
    path('dashboard/', views.tableau_de_bord, name='dashboard'),
]