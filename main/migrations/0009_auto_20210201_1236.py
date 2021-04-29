# Generated by Django 3.1.5 on 2021-02-01 12:36

import ckeditor.fields
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_catitems_ico'),
    ]

    operations = [
        migrations.CreateModel(
            name='PodCatItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias', models.SlugField(max_length=200, verbose_name='Url')),
                ('menushow', models.BooleanField(default=True, verbose_name='Показывать в меню')),
                ('sitemap', models.BooleanField(default=True, verbose_name='Показывать в карте сайта')),
                ('og_title', models.CharField(blank=True, max_length=200, null=True, verbose_name='OG Title')),
                ('og_description', models.TextField(blank=True, max_length=2000, null=True, verbose_name='OG Description')),
                ('og_type', models.CharField(blank=True, max_length=200, null=True, verbose_name='OG Type')),
                ('og_type_pb_time', models.DateField(default=datetime.date.today, verbose_name='Время публикации')),
                ('og_type_author', models.CharField(blank=True, max_length=200, null=True, verbose_name='OG author')),
                ('seo_h1', models.CharField(blank=True, max_length=200, null=True, verbose_name='H1')),
                ('seo_title', models.CharField(blank=True, max_length=200, null=True, verbose_name='Title')),
                ('seo_description', models.CharField(blank=True, max_length=500, null=True, verbose_name='Description')),
                ('seo_keywords', models.CharField(blank=True, max_length=500, null=True, verbose_name='Keywords')),
                ('menutitle', models.CharField(blank=True, max_length=200, null=True, verbose_name='Название в меню')),
                ('content', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Статья')),
                ('menuposition', models.IntegerField(blank=True, null=True, verbose_name='Позиция в меню')),
                ('lastmod', models.DateTimeField(auto_now=True, verbose_name='date_published')),
                ('canonical', models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='canonical')),
                ('name', models.CharField(max_length=200, verbose_name='Название услуги')),
                ('img_front', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Превью категории')),
                ('ico', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Иконка в меню')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.catitems', verbose_name='Категория товара')),
            ],
            options={
                'verbose_name': 'Категории для товаров',
                'verbose_name_plural': 'Категории для товаров',
            },
        ),
        migrations.AddField(
            model_name='item',
            name='pod_cat_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.podcatitems', verbose_name='Под категория товара'),
        ),
    ]
