# Generated by Django 3.1.5 on 2021-02-09 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_auto_20210209_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Цена п.м.'),
        ),
        migrations.AlterField(
            model_name='item',
            name='price_kv',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Цена кв.м'),
        ),
    ]