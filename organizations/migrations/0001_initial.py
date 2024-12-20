# Generated by Django 5.1.2 on 2024-10-23 19:19

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='نام سازمان یا مجموعه')),
                ('responsible_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='نام و نام خانوادگی مسئول')),
                ('responsible_phone', models.CharField(blank=True, max_length=15, null=True, verbose_name='شماره تماس مسئول')),
                ('national_id', models.CharField(blank=True, max_length=11, null=True, verbose_name='کد ملی مسئول')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='تاریخ ایجاد')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات درباره سازمان یا مجموعه')),
            ],
            options={
                'verbose_name': 'سازمان',
                'verbose_name_plural': 'سازمان\u200cها',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='نام گروه')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='تاریخ ایجاد')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات درباره گروه')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='organizations.organization', verbose_name='سازمان')),
            ],
            options={
                'verbose_name': 'گروه',
                'verbose_name_plural': 'گروه\u200cها',
            },
        ),
    ]
