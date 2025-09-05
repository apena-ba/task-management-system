from django.contrib.auth.models import AbstractUser
from django.db import models


class Team(models.Model):
    """
    Represents a team of users.
    Each team has one lead.
    """
    # Core fields
    name = models.CharField(max_length=100, unique=True)
    
    # Relationships
    lead = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="leading_team",
        help_text="User who leads the team",
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "teams"
        ordering = ["name"]

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Each user can belong to one team.
    """

    # Relationships
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="members",
        help_text="Team this user belongs to",
    )

    class Meta:
        db_table = "users"
        ordering = ["username"]

    def __str__(self):
        return self.username
