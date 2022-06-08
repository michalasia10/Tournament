from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class GameEnum(models.TextChoices):
    CHESS = 'CHESS', 'CHESS'
    FOOTBALL = 'FOOTBALL', 'FOOTBALL',
    BASKETBALL = 'BASKETBALL', 'BASKETBALL'


class Tournament(models.Model):
    name = models.CharField(max_length=250, unique=True)
    game_type = models.CharField(max_length=100, choices=GameEnum.choices, default=GameEnum.CHESS)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    max_teams = models.IntegerField(default=3, )
    max_players = models.IntegerField(default=2, validators=[MinValueValidator(2), MaxValueValidator(100)])
