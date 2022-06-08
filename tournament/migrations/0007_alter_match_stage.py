# Generated by Django 4.0.5 on 2022-06-06 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0006_stage_stage_part_tournament_max_stages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='stage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='tournament.stage', verbose_name='matches'),
        ),
    ]
