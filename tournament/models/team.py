from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=250)
    color = models.CharField(default='#FF0000',max_length=7)

