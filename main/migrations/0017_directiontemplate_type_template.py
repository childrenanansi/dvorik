# Generated by Django 3.1.5 on 2021-02-08 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_directiontemplate'),
    ]

    operations = [
        migrations.AddField(
            model_name='directiontemplate',
            name='type_template',
            field=models.IntegerField(choices=[(1, 'Категория'), (2, 'Товар')], default=1, verbose_name='Тип Шаблона'),
        ),
    ]
