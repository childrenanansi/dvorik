# Generated by Django 3.1.5 on 2021-02-11 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20210209_1046'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favicon', models.FileField(blank=True, null=True, upload_to='', verbose_name='Фавикон')),
                ('metrics_yandex', models.CharField(blank=True, max_length=100, null=True, verbose_name='Счетчик Яндекс')),
                ('metrics_google', models.CharField(blank=True, max_length=100, null=True, verbose_name='Счетчик Google')),
                ('robots', models.TextField(blank=True, max_length=3000, verbose_name='Robots.txt')),
                ('header_additional', models.TextField(blank=True, max_length=10000, verbose_name='Дополнения в <header>')),
            ],
            options={
                'verbose_name': 'Настройка сайта',
                'verbose_name_plural': 'Настройки сайта',
            },
        ),
    ]