# Generated by Django 5.1.2 on 2024-10-31 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='groups',
        ),
    ]
