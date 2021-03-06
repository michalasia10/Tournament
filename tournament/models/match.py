from django.db import models

from tournament.models import Team, Stage, StatusEnum
from tournament.validators.match import JSONMatchSchemaValidator
from tournament.validators.schemas import MATCH_JSON_SCHEMA


class Match(models.Model):
    team_a = models.OneToOneField(Team, models.CASCADE, unique=True, verbose_name="teamA", related_name='team_a')
    team_b = models.OneToOneField(Team, models.CASCADE, unique=True, verbose_name="teamB", related_name='team_b')
    score = models.JSONField(default=dict, null=True, blank=True,
                             validators=[JSONMatchSchemaValidator(limit_value=MATCH_JSON_SCHEMA)])
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='matches', verbose_name='matches')
    status = models.CharField(max_length=250, choices=StatusEnum.choices, default=StatusEnum.START.value)
