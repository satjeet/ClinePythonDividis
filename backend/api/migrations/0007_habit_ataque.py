# Generated by Django 5.2.1 on 2025-06-23 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_declaration_pillar_wellnesssurveyanswer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='habit',
            name='ataque',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=5),
        ),
    ]
