from django.contrib import admin
from .models import Filiere, Niveau, Matiere, Ressource, Signalement


@admin.register(Filiere)
class FiliereAdmin(admin.ModelAdmin):
    list_display = ('nom', 'code')
    search_fields = ('nom', 'code')


@admin.register(Niveau)
class NiveauAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'ordre')
    list_editable = ('ordre',)


@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ('nom', 'filiere', 'niveau')
    list_filter = ('filiere', 'niveau')
    search_fields = ('nom',)


@admin.register(Ressource)
class RessourceAdmin(admin.ModelAdmin):
    list_display = (
        'titre', 'matiere', 'type_document', 'annee_academique',
        'statut', 'depose_par', 'date_depot'
    )
    list_filter = ('statut', 'type_document', 'filiere', 'niveau', 'annee_academique')
    search_fields = ('titre', 'description')
    readonly_fields = ('date_depot', 'nb_telechargements')
    date_hierarchy = 'date_depot'


@admin.register(Signalement)
class SignalementAdmin(admin.ModelAdmin):
    list_display = ('ressource', 'motif', 'signale_par', 'date', 'traite')
    list_filter = ('motif', 'traite')
    search_fields = ('ressource__titre',)