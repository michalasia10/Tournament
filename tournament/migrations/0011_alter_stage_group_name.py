# Generated by Django 4.0.5 on 2022-06-06 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0010_alter_stage_winner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stage',
            name='group_name',
            field=models.CharField(max_length=250),
        ),
    ]
