from django.conf import settings
from django.db import models


class Filiere(models.Model):
    nom = models.CharField(max_length=100, unique=True, verbose_name="Nom")
    code = models.CharField(max_length=20, unique=True, verbose_name="Code (ex. GL)")

    class Meta:
        verbose_name = "Filière"
        verbose_name_plural = "Filières"
        ordering = ['nom']

    def __str__(self):
        return self.nom


class Niveau(models.Model):
    libelle = models.CharField(max_length=50, unique=True, verbose_name="Libellé (ex. Bac 2)")
    ordre = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")

    class Meta:
        verbose_name = "Niveau"
        verbose_name_plural = "Niveaux"
        ordering = ['ordre', 'libelle']

    def __str__(self):
        return self.libelle


class Matiere(models.Model):
    nom = models.CharField(max_length=150, verbose_name="Nom")
    filiere = models.ForeignKey(
        Filiere, on_delete=models.CASCADE,
        related_name='matieres', verbose_name="Filière"
    )
    niveau = models.ForeignKey(
        Niveau, on_delete=models.CASCADE,
        related_name='matieres', verbose_name="Niveau"
    )

    class Meta:
        verbose_name = "Matière"
        verbose_name_plural = "Matières"
        unique_together = [['nom', 'filiere', 'niveau']]
        ordering = ['nom']

    def __str__(self):
        return f"{self.nom} — {self.filiere.code} {self.niveau.libelle}"


class Ressource(models.Model):
    """Document pédagogique déposé sur la plateforme."""

    class TypeDocument(models.TextChoices):
        SYLLABUS = 'SYLLABUS', 'Syllabus'
        NOTES = 'NOTES', 'Notes de cours'
        TD = 'TD', 'TD'
        TP = 'TP', 'TP'
        EXAMEN = 'EXAMEN', 'Examen'
        CORRIGE = 'CORRIGE', 'Corrigé'
        RESUME = 'RESUME', 'Résumé'
        AUTRE = 'AUTRE', 'Autre'

    class Statut(models.TextChoices):
        EN_ATTENTE = 'EN_ATTENTE', 'En attente'
        PUBLIE = 'PUBLIE', 'Publié'
        REJETE = 'REJETE', 'Rejeté'
        RETIRE = 'RETIRE', 'Retiré'

    titre = models.CharField(max_length=200, verbose_name="Titre")
    filiere = models.ForeignKey(
        Filiere, on_delete=models.PROTECT,
        related_name='ressources', verbose_name="Filière"
    )
    niveau = models.ForeignKey(
        Niveau, on_delete=models.PROTECT,
        related_name='ressources', verbose_name="Niveau"
    )
    matiere = models.ForeignKey(
        Matiere, on_delete=models.PROTECT,
        related_name='ressources', verbose_name="Matière"
    )
    type_document = models.CharField(
        max_length=20, choices=TypeDocument.choices, verbose_name="Type de document"
    )
    annee_academique = models.CharField(
        max_length=9,
        verbose_name="Année académique",
        help_text="Format AAAA-AAAA (ex. 2023-2024)"
    )
    semestre = models.CharField(max_length=10, blank=True, verbose_name="Semestre")
    enseignant_nom = models.CharField(max_length=150, blank=True, verbose_name="Nom de l'enseignant")
    description = models.TextField(blank=True, verbose_name="Description")

    fichier = models.FileField(upload_to='ressources/%Y/%m/', verbose_name="Fichier")
    taille = models.PositiveIntegerField(default=0, verbose_name="Taille (octets)")
    format_fichier = models.CharField(max_length=10, blank=True, verbose_name="Format")

    date_depot = models.DateTimeField(auto_now_add=True, verbose_name="Date de dépôt")
    statut = models.CharField(
        max_length=20, choices=Statut.choices,
        default=Statut.EN_ATTENTE, verbose_name="Statut"
    )
    badge_officiel = models.BooleanField(default=False, verbose_name="Badge officiel")
    motif_rejet = models.TextField(blank=True, verbose_name="Motif de rejet")
    nb_telechargements = models.PositiveIntegerField(default=0, verbose_name="Téléchargements")

    depose_par = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='ressources_deposees', verbose_name="Déposé par"
    )

    class Meta:
        verbose_name = "Ressource"
        verbose_name_plural = "Ressources"
        ordering = ['-date_depot']
        indexes = [
            models.Index(fields=['statut', 'annee_academique']),
            models.Index(fields=['filiere', 'niveau']),
        ]

    def __str__(self):
        return f"{self.titre} ({self.annee_academique})"


class Signalement(models.Model):
    class Motif(models.TextChoices):
        ERRONE = 'ERRONE', 'Contenu erroné'
        HORS_SUJET = 'HORS_SUJET', 'Hors sujet'
        DOUBLON = 'DOUBLON', 'Doublon'
        ILLICITE = 'ILLICITE', 'Contenu illicite'
        AUTRE = 'AUTRE', 'Autre'

    ressource = models.ForeignKey(
        Ressource, on_delete=models.CASCADE,
        related_name='signalements', verbose_name="Ressource"
    )
    signale_par = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='signalements_emis', verbose_name="Signalé par"
    )
    motif = models.CharField(max_length=20, choices=Motif.choices, verbose_name="Motif")
    commentaire = models.TextField(blank=True, verbose_name="Commentaire")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date")
    traite = models.BooleanField(default=False, verbose_name="Traité")

    class Meta:
        verbose_name = "Signalement"
        verbose_name_plural = "Signalements"
        ordering = ['-date']

    def __str__(self):
        return f"Signalement : {self.ressource.titre} ({self.get_motif_display()})"
