# Generated by Django 5.1.2 on 2024-11-05 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
        ('text_messages', '0002_message_groups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='groups',
            field=models.ManyToManyField(blank=True, null=True, to='organizations.group', verbose_name='گروه\u200cهای مرتبط'),
        ),
    ]
