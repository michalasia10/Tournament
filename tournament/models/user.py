from django.db import models
from django.contrib.auth.models import User
from tournament.models import Team
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User,unique=True,on_delete=models.CASCADE)
    birth = models.DateTimeField()
    is_admin = models.BooleanField(default=False)
    team = models.ForeignKey(Team,related_name='players',on_delete=models.CASCADE,null=True,blank=True,default=None)

