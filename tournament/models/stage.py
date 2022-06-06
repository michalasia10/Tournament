from django.db import models

from tournament.models import Team, Tournament


class Stage(models.Model):
    stage_part = models.IntegerField(unique=False, default=0)
    group_name = models.CharField(max_length=250, unique=False)
    winner = models.OneToOneField(Team, unique=True, on_delete=models.CASCADE, blank=True, null=True)
    tourament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='stages')
