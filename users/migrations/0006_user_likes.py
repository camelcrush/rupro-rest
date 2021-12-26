# Generated by Django 3.0 on 2021-12-26 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20211226_2122'),
        ('users', '0005_auto_20211226_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likes', to='posts.Post'),
        ),
    ]
