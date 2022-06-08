from django.contrib.auth.models import User
from django.db import models

from tournament.models import Team


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, related_name='user_profile')
    birth = models.DateTimeField()
    is_admin = models.BooleanField(default=False)
    team = models.ForeignKey(Team, related_name='players', on_delete=models.CASCADE, null=True, blank=True,
                             default=None)
