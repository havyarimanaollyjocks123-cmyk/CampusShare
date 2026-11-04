from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Utilisateur CampusShare : étudiant, délégué, enseignant ou administrateur."""
    def save(self, *args, **kwargs):
        # Si l'utilisateur est superuser, on force son rôle à ADMIN
        if self.is_superuser:
            self.role = self.Role.ADMIN
        super().save(*args, **kwargs)

    class Role(models.TextChoices):
        ETUDIANT = 'ETUDIANT', 'Étudiant'
        DELEGUE = 'DELEGUE', 'Délégué'
        ENSEIGNANT = 'ENSEIGNANT', 'Enseignant'
        ADMIN = 'ADMIN', 'Administrateur'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.ETUDIANT,
        verbose_name="Rôle"
    )
    filiere = models.ForeignKey(
        'catalog.Filiere',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='etudiants',
        verbose_name="Filière"
    )
    niveau = models.ForeignKey(
        'catalog.Niveau',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='etudiants',
        verbose_name="Niveau"
    )

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        nom_complet = self.get_full_name() or self.username
        return f"{nom_complet} ({self.get_role_display()})"