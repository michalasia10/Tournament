from django.db import models
from tournament.models import Team, Tournament

class Stage(models.Model):
    group_name = models.CharField(max_length=250,unique=True)
    winner = models.OneToOneField(Team,unique=True,on_delete=models.CASCADE)
    tourament = models.ForeignKey(Tournament,on_delete=models.CASCADE,related_name='stages')