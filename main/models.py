from __future__ import unicode_literals

import datetime

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse, reverse_lazy
from ckeditor.fields import RichTextField


class Page(models.Model):
    class Meta:
        abstract = True

    alias = models.SlugField(max_length=200, verbose_name=u"Url")
    menushow = models.BooleanField(
        default=True, verbose_name=u"Показывать в меню")
    sitemap = models.BooleanField(
        default=True, verbose_name=u"Показывать в карте сайта")
    og_title = models.CharField(
        max_length=200, verbose_name="OG Title", null=True, blank=True)
    og_description = models.TextField(
        max_length=2000, verbose_name="OG Description", null=True, blank=True)
    og_type = models.CharField(
        max_length=200, verbose_name="OG Type", null=True, blank=True)
    og_type_pb_time = models.DateField(
        default=datetime.date.today, verbose_name=u"Время публикации")
    og_type_author = models.CharField(
        max_length=200, verbose_name="OG author", null=True, blank=True)
    seo_h1 = models.CharField(
        max_length=200, verbose_name="H1", null=True, blank=True)
    seo_title = models.CharField(
        max_length=200, verbose_name="Title", null=True, blank=True)
    seo_description = models.CharField(
        max_length=500, verbose_name="Description", null=True, blank=True)
    seo_keywords = models.CharField(
        max_length=500, verbose_name="Keywords", null=True, blank=True)
    menutitle = models.CharField(
        max_length=200, verbose_name=u"Название в меню", null=True, blank=True)
    content = RichTextField(verbose_name=u"Статья", null=True, blank=True)
    menuposition = models.IntegerField(
        verbose_name=u"Позиция в меню", null=True, blank=True)
    lastmod = models.DateTimeField('date_published', auto_now=True)
    canonical = models.CharField(max_length=500, verbose_name=u"canonical", default='', null=True, blank=True)

class Settings(models.Model):
    class Meta:
        verbose_name = "Настройка сайта"
        verbose_name_plural = "Настройки сайта"

    favicon = models.FileField(verbose_name=u"Фавикон", null=True, blank=True)
    metrics_yandex = models.CharField(
        max_length=100, verbose_name='Счетчик Яндекс', null=True, blank=True)
    phone = models.CharField(
        max_length=100, verbose_name='Телефон', null=True, blank=True)
    address = models.CharField(
        max_length=100, verbose_name='Адрес', null=True, blank=True)
    metrics_google = models.CharField(
        max_length=100, verbose_name='Счетчик Google', null=True, blank=True)
    robots = models.TextField(
        verbose_name="Robots.txt", max_length=3000, blank=True)
    header_additional = models.TextField(
        verbose_name="Дополнения в <header>", max_length=10000, blank=True)

class TextPage(Page):
    class Meta:
        verbose_name = u"Текстовая страница"
        verbose_name_plural = u"Страницы"

    name = models.CharField(max_length=200, verbose_name=u"Название")
    is_service = models.BooleanField(verbose_name="Услуга?", default=False)
    img_path = models.ImageField(verbose_name='Изображение для yandex turbo', default='', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        if self.alias == "index":
            return reverse('main:index', kwargs={})
        else:
            postfix = 'servicepage' if self.is_service else 'textpage'
            return reverse("main:{}".format(postfix), kwargs={'alias': self.alias})


class CatProject(Page):
    class Meta:
        verbose_name = u"Категории проектов"
        verbose_name_plural = u"Категории проектов"
        ordering = ['menuposition']

    name = models.CharField(max_length=200, verbose_name=u"Название услуги")

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('main:raboti')


class Project(Page):
    class Meta:
        verbose_name = u"Проекты"
        verbose_name_plural = u"Проекты"

    name = models.CharField(max_length=200, verbose_name=u"Название услуги")
    cat = models.ForeignKey(CatProject, verbose_name='Категория', on_delete=models.CASCADE, null=True, blank=True)
    img_front = models.ImageField(verbose_name='Основное Изображение', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main:raboti_item', kwargs={'alias': self.alias})

class Slider(models.Model):
    class Meta:
        verbose_name = u"Изображения для слайдеров"
        verbose_name_plural = u"Изображения для слайдеров"

    name = models.CharField(max_length=200, verbose_name=u"alt Изображения")
    image = models.ImageField(verbose_name='Изображение', null=True, blank=True)
    display_home = models.BooleanField(default=False, verbose_name="Отображать на главной?")
    project = models.ForeignKey(Project, verbose_name='Проекты', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class CatItems(Page):
    class Meta:
        verbose_name = u"Категории для товаров"
        verbose_name_plural = u"Категории для товаров"
        ordering = ['menuposition']

    name = models.CharField(max_length=200, verbose_name=u"Название услуги")
    img_front = models.ImageField(verbose_name='Превью категории', null=True, blank=True)
    ico = models.ImageField(verbose_name='Иконка в меню', null=True, blank=True)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('main:catalog_item', kwargs={'alias': self.alias})

class PodCatItems(Page):
    class Meta:
        verbose_name = u"Под категории для товаров"
        verbose_name_plural = u"Под категории для товаров"
        ordering = ['menuposition']

    name = models.CharField(max_length=200, verbose_name=u"Название услуги")
    img_front = models.ImageField(verbose_name='Превью категории', null=True, blank=True)
    ico = models.ImageField(verbose_name='Иконка в меню', null=True, blank=True)
    parent = models.ForeignKey(CatItems, verbose_name='Категория товара', on_delete=models.SET_NULL, null=True,
                                 blank=True)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('main:catalog_item_item', kwargs={'parent': self.parent.alias, 'alias': self.alias})

class Item(Page):
    class Meta:
        verbose_name = u"Товары"
        verbose_name_plural = u"Товары"
        ordering = ['menuposition']

    img_front = models.ImageField(verbose_name='Основное Изображение', null=True, blank=True)
    name = models.CharField(max_length=200, verbose_name=u"Название услуги")
    size = models.CharField(max_length=200, verbose_name=u"Размер мм", null=True, blank=True)
    dlina = models.CharField(max_length=200, verbose_name=u"Длина (с указанием ед.измерения)", null=True, blank=True)
    obrob = models.CharField(max_length=200, verbose_name=u"Обработка", null=True, blank=True)
    price = models.FloatField(default=0, verbose_name='Цена п.м.', null=True, blank=True)
    price_kv = models.FloatField(default=0, verbose_name='Цена кв.м', null=True, blank=True)
    des_right = RichTextField(verbose_name=u"Описание в правой части товара", null=True, blank=True)
    published = models.BooleanField(default=False, verbose_name="Опубликовано (показывать на сайте)")
    show_on_index = models.BooleanField(default=False, verbose_name="Показывать на главной")
    label_new = models.BooleanField(default=False, verbose_name="Новика?")
    label_hit = models.BooleanField(default=False, verbose_name="Хит?")
    cat_item = models.ForeignKey(CatItems, verbose_name='Категория товара', on_delete=models.SET_NULL, null=True, blank=True)
    pod_cat_item = models.ForeignKey(PodCatItems, verbose_name='Под категория товара', on_delete=models.SET_NULL, null=True, blank=True)
    price_for_wt = models.BooleanField(default=False, verbose_name="Цена за штуку?")

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('main:product', kwargs={'alias': self.alias})

class Upsell(models.Model):
    class Meta:
        verbose_name = u"Похожие товары"
        verbose_name_plural = u"Похожие товары"

    item = models.ForeignKey(Item, verbose_name='К какому товару', on_delete=models.CASCADE, null=True, blank=True)
    ups = models.ManyToManyField(Item, verbose_name='Какие товары', related_name="upsellitem")

    def __str__(self):
        return self.item.name

class Crosssell(models.Model):
    class Meta:
        verbose_name = u"Сопутствующие товары"
        verbose_name_plural = u"Сопутствующие товары"

    item = models.ForeignKey(Item, verbose_name='К какому товару', on_delete=models.CASCADE, null=True, blank=True)
    cross = models.ManyToManyField(Item, verbose_name='Какие товары', related_name="crosselitem")

    def __str__(self):
        return self.item.name

class Img(Page):
    class Meta:
        verbose_name = u"Картинка товара"
        verbose_name_plural = u"Картинки товаров"

    name = models.CharField(max_length=200, verbose_name=u"Alt картинки")
    img = models.ImageField(verbose_name='Фото товара', default='', null=True, blank=True)
    item = models.ForeignKey(Item, verbose_name='Товар', on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.item.name

class Contacts(Page):
    class Meta:
        verbose_name = u"Контакт"
        verbose_name_plural = u"Контакты"

    name = models.CharField(max_length=200, verbose_name=u"Контакты")
    iframe = models.TextField(max_length=50000, verbose_name='Код Страницы из карт')
    address = models.CharField(max_length=1000, verbose_name='Адрес')
    telephone = models.CharField(max_length=100, verbose_name='Телефоны')
    email = models.CharField(max_length=100, verbose_name='Почта')

    def __str__(self):
        return self.name

temp_type = [
    (1, 'Категория'),
    (2, 'Товар')
]


class DirectionTemplate(Page):
    class Meta:
        verbose_name = u"Шаблон страниц категорий"
        verbose_name_plural = u"Шаблоны страниц категорий"

    name = models.CharField(
        max_length=500, verbose_name=u"Название шаблона", blank=True)
    type_template = models.IntegerField(default=1, choices=temp_type, verbose_name=u"Тип Шаблона")

    def __str__(self):
        return self.name

class Robots(models.Model):
    class Meta:
        verbose_name = u"Robots"
        verbose_name_plural = u"Robots"

    content = models.TextField(verbose_name=u"Содержимое")

    def __str__(self):
        return self.content


class Order(models.Model):
    class Meta:
        verbose_name = u"Заявка"
        verbose_name_plural = u"Заявки"

    name = models.CharField(max_length=200, verbose_name=u"Имя")
    item = models.ForeignKey(Item, verbose_name='Товар', on_delete=models.CASCADE, null=True, blank=True)
    telephone = models.CharField(max_length=100, verbose_name='Телефоны')
    email = models.CharField(max_length=100, verbose_name='Почта', null=True, blank=True)
    text = models.TextField(max_length=5000, verbose_name='Текст заявки', null=True, blank=True)

    def __str__(self):
        return self.name

