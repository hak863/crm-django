# Generated by Django 3.1 on 2024-01-10 22:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0013_lead_organisation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lead',
            name='organisation',
        ),
    ]
