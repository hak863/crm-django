# Generated by Django 3.1 on 2024-01-11 17:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0017_auto_20240111_2307'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='organisation',
        ),
    ]
