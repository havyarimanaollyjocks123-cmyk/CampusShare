# CampusShare 🎓

**Plateforme de centralisation et d'archivage des ressources pédagogiques universitaires.**

Réalisé dans le cadre de l'examen du cours d'Ingénierie Logicielle - Bac 2 Génie Logiciel.

## 🛠️ Stack Technique
- **Backend** : Django 5 (Python)
- **Frontend** : Templates Django + CSS artisanal (Responsive)
- **Base de données** : SQLite (Développement)

## 🚀 Fonctionnalités
- Authentification et gestion des rôles (Étudiant, Délégué, Enseignant, Admin).
- Dépôt de documents avec métadonnées (Filière, Niveau, Matière, Année Académique).
- Catalogue avec recherche multi-critères.
- Modération décentralisée (Délégués modèrent leur filière).
- Système de signalement et tableau de bord administrateur.

## 💻 Installation locale
1. Cloner le projet : `git clone https://github.com/TON_NOM/CampusShare.git`
2. Créer un environnement virtuel : `python -m venv venv`
3. Activer l'environnement : `venv\Scripts\activate` (Windows)
4. Installer les dépendances : `pip install django pillow`
5. Appliquer les migrations : `python manage.py migrate`
6. Lancer le serveur : `python manage.py runserver`
