from django.db import models
from tournament.models import Team,Stage

class Match(models.Model):
    team_a = models.OneToOneField(Team,models.CASCADE,unique=True,verbose_name="teamA",related_name='team_a')
    team_b = models.OneToOneField(Team,models.CASCADE,unique=True,verbose_name="teamB",related_name='team_b')
    score = models.JSONField()
    stage = models.ForeignKey(Stage,on_delete=models.CASCADE,related_name='matches',verbose_name='matches')
