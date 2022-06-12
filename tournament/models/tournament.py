from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User


class GameEnum(models.TextChoices):
    CHESS = 'CHESS', 'CHESS'
    FOOTBALL = 'FOOTBALL', 'FOOTBALL',
    BASKETBALL = 'BASKETBALL', 'BASKETBALL'


class StatusEnum(models.TextChoices):
    START = 'START', 'START'
    IN_PROGRESS = 'IN_PROGRESS', 'IN_PROGRESS'
    END = "END", "END"


class Tournament(models.Model):
    name = models.CharField(max_length=250, unique=True)
    game_type = models.CharField(max_length=100, choices=GameEnum.choices, default=GameEnum.CHESS)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    max_teams = models.IntegerField(default=3, )
    max_players = models.IntegerField(default=2, validators=[MinValueValidator(2), MaxValueValidator(100)])
    status = models.CharField(max_length=250, choices=StatusEnum.choices, default='')
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='torunaments',default=1)
