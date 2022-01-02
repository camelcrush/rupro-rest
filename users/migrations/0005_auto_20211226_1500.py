# Generated by Django 3.0 on 2021-12-26 06:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_auto_20211128_1412'),
        ('users', '0004_auto_20211129_2256'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='blocked_user',
            field=models.ManyToManyField(blank=True, related_name='blocked_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='following_user',
            field=models.ManyToManyField(blank=True, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='game_list',
            field=models.ManyToManyField(blank=True, to='games.Game'),
        ),
    ]