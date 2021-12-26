# Generated by Django 3.0 on 2021-11-28 02:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
        ('boards', '0002_board_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='boards', to='games.Game'),
        ),
    ]
