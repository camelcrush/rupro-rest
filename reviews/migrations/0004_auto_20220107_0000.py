# Generated by Django 3.0 on 2022-01-06 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gamescores', '0002_gamescore_user'),
        ('reviews', '0003_auto_20220106_2357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='reviewed_game_score',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='gamescores.GameScore'),
        ),
    ]
