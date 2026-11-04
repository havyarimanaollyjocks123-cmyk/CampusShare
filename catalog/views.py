from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RessourceForm
from .models import Ressource
import os
from django.shortcuts import get_object_or_404
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q


@login_required
def depot_ressource(request):
    if request.method == 'POST':
        form = RessourceForm(request.POST, request.FILES)
        if form.is_valid():
            ressource = form.save(commit=False)
            ressource.depose_par = request.user
            
            # Métadonnées du fichier
            fichier = request.FILES['fichier']
            ressource.taille = fichier.size
            ressource.format_fichier = os.path.splitext(fichier.name)[1].lower()
            
            # Règle de gestion RG1 (Enseignant/Délégué = publié, Étudiant = en attente)
            if request.user.role in ['ENSEIGNANT', 'DELEGUE', 'ADMIN']:
                ressource.statut = Ressource.Statut.PUBLIE
                if request.user.role == 'ENSEIGNANT':
                    ressource.badge_officiel = True
            else:
                ressource.statut = Ressource.Statut.EN_ATTENTE
            
            ressource.save()
            messages.success(request, "Votre ressource a bien été enregistrée !")
            return redirect('mes_depots')
    else:
        form = RessourceForm()
    
    return render(request, 'catalog/depot.html', {'form': form})

@login_required
def mes_depots(request):
    ressources = Ressource.objects.filter(depose_par=request.user).order_by('-date_depot')
    return render(request, 'catalog/mes_depots.html', {'ressources': ressources})



@login_required
def file_attente(request):
    # Seuls l'admin et les délégués voient la file d'attente
    if request.user.role not in ['ADMIN', 'DELEGUE'] and not request.user.is_superuser:
        messages.error(request, "Vous n'avez pas l'autorisation de modérer les ressources.")
        return redirect('accueil')
    
    # On récupère les ressources en attente
    ressources = Ressource.objects.filter(statut=Ressource.Statut.EN_ATTENTE).order_by('-date_depot')
    return render(request, 'catalog/moderation.html', {'ressources': ressources})

@login_required
def valider_ressource(request, ressource_id, action):
    if request.user.role not in ['ADMIN', 'DELEGUE'] and not request.user.is_superuser:
        return redirect('accueil')
        
    ressource = get_object_or_404(Ressource, id=ressource_id)
    
    if action == 'valider':
        ressource.statut = Ressource.Statut.PUBLIE
        messages.success(request, f"La ressource '{ressource.titre}' a été publiée.")
    elif action == 'rejeter':
        ressource.statut = Ressource.Statut.REJETE
        ressource.motif_rejet = "Non conforme aux règles de la plateforme." 
        messages.warning(request, f"La ressource '{ressource.titre}' a été rejetée.")
        
    ressource.save()
    return redirect('file_attente')

    from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

@login_required
def file_attente(request):
    # Seuls l'admin et les délégués voient la file d'attente
    if request.user.role not in ['ADMIN', 'DELEGUE'] and not request.user.is_superuser:
        messages.error(request, "Vous n'avez pas l'autorisation de modérer les ressources.")
        return redirect('accueil')
    
    # On récupère les ressources en attente
    ressources = Ressource.objects.filter(statut=Ressource.Statut.EN_ATTENTE).order_by('-date_depot')
    return render(request, 'catalog/moderation.html', {'ressources': ressources})

@login_required
def valider_ressource(request, ressource_id, action):
    if request.user.role not in ['ADMIN', 'DELEGUE'] and not request.user.is_superuser:
        return redirect('accueil')
        
    ressource = get_object_or_404(Ressource, id=ressource_id)
    
    if action == 'valider':
        ressource.statut = Ressource.Statut.PUBLIE
        messages.success(request, f"La ressource '{ressource.titre}' a été publiée.")
    elif action == 'rejeter':
        ressource.statut = Ressource.Statut.REJETE
        ressource.motif_rejet = "Non conforme aux règles de la plateforme." # On pourra améliorer ça plus tard
        messages.warning(request, f"La ressource '{ressource.titre}' a été rejetée.")
        
    ressource.save()
    return redirect('file_attente')

    # Pour voir la file d'attente de mon app

@login_required
def file_attente(request):
    # Vérifier si l'utilisateur a le droit de modérer
    if request.user.role not in ['ADMIN', 'DELEGUE'] and not request.user.is_superuser:
        messages.error(request, "Action non autorisée.")
        return redirect('accueil')
    
    # Récupérer uniquement les ressources en attente
    ressources = Ressource.objects.filter(statut=Ressource.Statut.EN_ATTENTE).order_by('-date_depot')
    return render(request, 'catalog/moderation.html', {'ressources': ressources})


# Valider ou rejeter la ressource

@login_required
def action_moderation(request, ressource_id, action):
    if request.user.role not in ['ADMIN', 'DELEGUE'] and not request.user.is_superuser:
        return redirect('accueil')
        
    ressource = get_object_or_404(Ressource, id=ressource_id)
    
    if action == 'valider':
        ressource.statut = Ressource.Statut.PUBLIE
        messages.success(request, f"La ressource a été publiée.")
    elif action == 'rejeter':
        ressource.statut = Ressource.Statut.REJETE
        ressource.motif_rejet = "Rejeté par l'administrateur." # On met un motif par défaut pour l'instant
        messages.warning(request, f"La ressource a été rejetée.")
        
    ressource.save()
    return redirect('file_attente')  
    
    # vue pour filtres les ressources 

def catalogue(request):
    # On ne récupère QUE les ressources publiées (RG2)
    ressources = Ressource.objects.filter(statut=Ressource.Statut.PUBLIE)
    
    # Récupération des filtres depuis l'URL (ex: ?filiere=1&niveau=2)
    q = request.GET.get('q', '')
    filiere_id = request.GET.get('filiere', '')
    niveau_id = request.GET.get('niveau', '')
    matiere_id = request.GET.get('matiere', '')
    type_doc = request.GET.get('type', '')
    annee = request.GET.get('annee', '')

    # Application des filtres
    if q:
        ressources = ressources.filter(Q(titre__icontains=q) | Q(description__icontains=q))
    if filiere_id:
        ressources = ressources.filter(filiere_id=filiere_id)
    if niveau_id:
        ressources = ressources.filter(niveau_id=niveau_id)
    if matiere_id:
        ressources = ressources.filter(matiere_id=matiere_id)
    if type_doc:
        ressources = ressources.filter(type_document=type_doc)
    if annee:
        ressources = ressources.filter(annee_academique__icontains=annee)

    # Pour remplir les menus déroulants
    from .models import Filiere, Niveau, Matiere
    filieres = Filiere.objects.all()
    niveaux = Niveau.objects.all()
    matieres = Matiere.objects.all()
    
    # Liste des types de documents pour le filtre
    types_doc = Ressource.TypeDocument.choices

    context = {
        'ressources': ressources,
        'filieres': filieres,
        'niveaux': niveaux,
        'matieres': matieres,
        'types_doc': types_doc,
        'q': q,
    }
    return render(request, 'catalog/catalogue.html', context) 

# Vue de telechargement du document 

from django.http import FileResponse

@login_required
def telecharger_ressource(request, ressource_id):
    ressource = get_object_or_404(Ressource, id=ressource_id, statut=Ressource.Statut.PUBLIE)
    
    # Incrémenter le compteur (EF4.2)
    ressource.nb_telechargements += 1
    ressource.save()
    
    # Renvoyer le fichier
    try:
        return FileResponse(ressource.fichier.open('rb'), as_attachment=True)
    except FileNotFoundError:
        messages.error(request, "Le fichier est introuvable sur le serveur.")
        return redirect('catalogue')

# Cote admin

@login_required
def tableau_de_bord(request):
    if request.user.role != 'ADMIN' and not request.user.is_superuser:
        return redirect('accueil')
    
    total_ressources = Ressource.objects.filter(statut=Ressource.Statut.PUBLIE).count()
    en_attente = Ressource.objects.filter(statut=Ressource.Statut.EN_ATTENTE).count()
    total_telechargements = sum(r.nb_telechargements for r in Ressource.objects.all())
    
    return render(request, 'catalog/dashboard.html', {
        'total_ressources': total_ressources,
        'en_attente': en_attente,
        'total_telechargements': total_telechargements,
    })