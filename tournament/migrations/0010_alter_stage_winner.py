# Generated by Django 4.0.5 on 2022-06-06 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0009_remove_stage_name_remove_tournament_max_stages_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stage',
            name='winner',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tournament.team'),
        ),
    ]
