# Generated by Django 5.2.1 on 2025-06-27 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_habit_ataque'),
    ]

    operations = [
        migrations.AddField(
            model_name='mission',
            name='requirements',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
