from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import InscriptionForm, ConnexionForm

def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Bienvenue sur CampusShare ! Votre compte a été créé.")
            return redirect('accueil')
    else:
        form = InscriptionForm()
    return render(request, 'accounts/inscription.html', {'form': form})

def connexion(request):
    if request.method == 'POST':
        form = ConnexionForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Ravi de vous revoir, {user.first_name or user.username} !")
            return redirect('accueil')
    else:
        form = ConnexionForm()
    return render(request, 'accounts/connexion.html', {'form': form})

def deconnexion(request):
    logout(request)
    messages.info(request, "Vous êtes déconnecté.")
    return redirect('connexion')

@login_required
def profil(request):
    if request.method == 'POST':
        # On récupère la photo envoyée
        photo = request.FILES.get('photo_profil')
        if photo:
            request.user.photo_profil = photo
            request.user.save()
            messages.success(request, "Votre photo de profil a été mise à jour !")
            return redirect('profil')
            
    return render(request, 'accounts/profil.html')