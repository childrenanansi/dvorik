import json
import logging
import time
from http import HTTPStatus
from django.views.decorators.csrf import csrf_exempt
import requests
from telega.views import *
from django.http import Http404
from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib.sitemaps import Sitemap
from django.template import loader, Context, Template
from django.utils.functional import cached_property
from django.contrib.sites.requests import RequestSite
from django.contrib.sitemaps.views import x_robots_tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.template.context_processors import csrf
from django.utils.text import slugify
from django.template.response import TemplateResponse
from unidecode import unidecode
from .models import *
from telega.models import *

def default_context(request):
    """ Default template context. """
    csrf_token = dict(csrf(request))
    menu_top = list(TextPage.objects.filter(menushow=True))
    settings = Settings.objects.last()
    context_object = {"c": csrf_token,
                      'header_additional': settings.header_additional,
                      'favicon': settings.favicon,
                      'metrics_yandex': settings.metrics_yandex,
                      'metrics_google': settings.metrics_google,
                      'phone': settings.phone,
                      'address': settings.address,
                      'robots': settings.robots,
                      "menu_top": menu_top}
    return context_object

def render_textpage(request, alias, object):
    default_context_d = default_context(request)

    # Caution: If there's no specified object, it returns 404
    textpage_data = get_object_or_404(object, alias=alias)
    textpage_context = {"data": textpage_data}
    if textpage_data.canonical:
        canonical = textpage_data.canonical
    else:
        canonical = '{}{}'.format(request.get_host(), request.path)
    akcii = {"akcii": Akcii.objects.filter(textpage__id=textpage_data.id)}
    banner = {"banner": Banner.objects.filter(textpage__id=textpage_data.id)}
    canonical_obj = {'canonical': canonical}
    context = dict(default_context_d, **canonical_obj)
    context = dict(context, **akcii)
    context = dict(context, **banner)
    context = dict(context, **textpage_context)
    menu_obj = {'menu': CatItems.objects.all()}
    context = dict(context, **menu_obj)
    try:
        template = loader.get_template("{}.html".format(alias))
        return context, template
    except Exception:
        template = loader.get_template("default.html")
        return context, template

def page_404(request, exception=None):
    return redirect('/404.html')

def index(request):
    textpage_data, template = render_textpage(request, "index", TextPage)
    return HttpResponse(
        template.render({
            **textpage_data,
            'items': Item.objects.filter(show_on_index=True),
            'projects': Project.objects.all()[:4],
            'sliders': Slider.objects.filter(display_home=True),
        }))

def index_home(request):
    return redirect('/')

def contact(request):
    textpage_data, template = render_textpage(request, "contact", TextPage)
    return HttpResponse(
        template.render({
            **textpage_data
        }))

def delivery(request):
    textpage_data, template = render_textpage(request, "delivery", TextPage)
    return HttpResponse(
        template.render({
            **textpage_data
        }))

def optovikam(request):
    textpage_data, template = render_textpage(request, "optovikam", TextPage)
    return HttpResponse(
        template.render({
            **textpage_data,
            'items': Item.objects.filter(show_on_index=True),
        }))

def sitemap_xml(request):
    template = loader.get_template('sitemap_xml.html')

    host = 'https://{}/'.format(request.get_host())

    context = {
        'host': host,
        'catalog': CatItems.objects.all(),
        'pod_catalog': PodCatItems.objects.all(),
        'items': Item.objects.all(),
        'works': Project.objects.all(),
        'pages_index': TextPage.objects.get(alias='index'),
        'pages': TextPage.objects.exclude(alias='index').all(),
    }

    return HttpResponse(template.render(context), content_type='application/xhtml+xml')

def textpage(request, alias):
    textpage_data, template = render_textpage(request, alias, TextPage)
    return HttpResponse(template.render(textpage_data))

def raboti(request):
    textpage_data, template = render_textpage(request, "raboti", TextPage)
    print(textpage_data)
    select_cat = ''
    cat_name = None
    if request.GET.get('sort') == 'desc':
        ordering = '-lastmod'
        ord = 'desc'
    else:
        ord = 'asc'
        ordering = 'lastmod'
    if request.GET.get('cat_f') and request.GET.get('cat_f') != 'all':
        select_cat = request.GET.get('cat_f')
        if request.GET.get('cat_f') != 'all':
            cat_name = CatProject.objects.get(alias=request.GET.get('cat_f'))
        if ordering:
            projects = Project.objects.select_related('cat').filter(cat__alias=request.GET.get('cat_f')).all().order_by(ordering)
        else:
            projects = Project.objects.select_related('cat').filter(cat__alias=request.GET.get('cat_f')).all()
    else:
        if ordering:
            projects = Project.objects.select_related('cat').all().order_by(ordering)
        else:
            projects = Project.objects.select_related('cat').all()
    cat_project = CatProject.objects.all()
    paginator = Paginator(projects, 12)
    page = request.GET.get('page')
    pages = 1
    first_pages = 1
    count = projects.count()
    try:
        page_obj = paginator.page(page)
        if count >= int(page) * 12:
            pages = int(page) * 12
            first_pages = int(pages) - 12 + 1
        else:
            pages = count
    except PageNotAnInteger:
        page_obj = paginator.page(1)
        pages = 1 * 12
        first_pages = pages - 12 + 1
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return HttpResponse(
        template.render({
            **textpage_data,
            'pag': page_obj,
            'pages': pages,
            'order': ord,
            'cat_name': cat_name,
            'select_cat': select_cat,
            'first_pages': first_pages,
            'projects': projects,
            'catprojects': cat_project,
        }))

def raboti_item(request, alias):
    context, template = render_textpage(request, alias, Project)
    template = loader.get_template("raboti_item.html")
    project = Project.objects.get(alias=alias)
    f = 0
    alias = ''
    for p in Project.objects.all():
        if f == 1:
            f = 0
            alias = p.alias
        if p.alias == project.alias:
            f = 1
    return HttpResponse(template.render(dict({
        **context,
        'sliders': Slider.objects.filter(project=project),
        'project': project,
        'akcii': Akcii.objects.filter(textpage__id=TextPage.objects.get(alias='raboti').id),
        'catprojects': CatProject.objects.all(),
        'next': alias
    })))


def product(request, alias):
    context, template = render_textpage(request, alias, Item)
    template = loader.get_template("product.html")
    item = Item.objects.get(alias=alias)
    left_menu = PodCatItems.objects.filter(parent=item.cat_item)
    upsel = ''
    if Upsell.objects.filter(item=item).exists():
        upsel = Upsell.objects.get(item=item)
    cross = ''
    if Crosssell.objects.filter(item=item).exists():
        cross = Crosssell.objects.get(item=item)

    direction_template = DirectionTemplate.objects.filter(type_template=2).first()
    templated_payload = dict()
    templated_payload = {'item': item}
    templated_h1 = Template(
        direction_template.seo_h1).render(Context(templated_payload))
    templated_title = Template(
        direction_template.seo_title).render(Context(templated_payload))
    templated_description = Template(
        direction_template.seo_description).render(Context(templated_payload))
    templated_content = Template(
        direction_template.content).render(Context(templated_payload))
    templated_keywords = Template(
        direction_template.seo_keywords).render(Context(templated_payload))

    return HttpResponse(template.render(dict({
        **context,
        'item': item,
        'sliders': Img.objects.filter(item=item),
        'left_menu': left_menu,
        'upsel': upsel,
        'cross': cross,
        'templated_h1': templated_h1,
        'templated_title': templated_title,
        'templated_content': templated_content,
        'templated_keywords': templated_keywords,
        'templated_description': templated_description
    })))

def catalog_items(request, alias, parent=''):
    cat_items = ''
    pod_cat = ''
    if request.GET.get('sort') == 'desc':
        ordering = '-price'
        ord = 'desc'
        url_s = '?sort={}'.format(ord)
    else:
        ord = 'asc'
        ordering = 'price'
        url_s = '?sort={}'.format(ord)
    if CatItems.objects.filter(alias=alias).exists():
        context, template = render_textpage(request, alias, CatItems)
        cat_items = CatItems.objects.get(alias=alias)
        items = Item.objects.filter(cat_item=cat_items).select_related('cat_item', 'pod_cat_item').order_by(ordering)
    elif PodCatItems.objects.filter(alias=alias).exists():
        context, template = render_textpage(request, alias, PodCatItems)
        pod_cat = PodCatItems.objects.select_related('parent').get(alias=alias)
        items = Item.objects.filter(pod_cat_item=pod_cat).select_related('cat_item', 'pod_cat_item').order_by(ordering)
        cat_items = pod_cat.parent
    else:
        raise Http404()
    left_menu = ''
    if cat_items:
        left_menu = PodCatItems.objects.select_related('parent').filter(parent=cat_items)
    template = loader.get_template("catalog_items.html")
    paginator = Paginator(items, 12)
    page = request.GET.get('page')
    pages = 1
    first_pages = 1
    count = items.count()
    try:
        page_obj = paginator.page(page)
        if count >= int(page) * 12:
            pages = int(page) * 12
            first_pages = int(pages) - 12 + 1
        else:
            pages = count
    except PageNotAnInteger:
        page_obj = paginator.page(1)
        pages = 1 * 12
        first_pages = pages - 12 + 1
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    direction_template = DirectionTemplate.objects.filter(type_template=1).first()
    templated_payload = dict()
    min_price = 0
    for item in items:
        if min_price == 0:
            min_price = item.price
        elif min_price > item.price:
            min_price = item.price
    if pod_cat:
        templated_payload = {'cat': pod_cat, 'min_price': min_price}
    else:
        templated_payload = {'cat': cat_items, 'min_price': min_price}
    templated_h1 = Template(
        direction_template.seo_h1).render(Context(templated_payload))
    templated_title = Template(
        direction_template.seo_title).render(Context(templated_payload))
    templated_description = Template(
        direction_template.seo_description).render(Context(templated_payload))
    templated_content = Template(
        direction_template.content).render(Context(templated_payload))
    templated_keywords = Template(
        direction_template.seo_keywords).render(Context(templated_payload))

    doted_end = False
    if page_obj.paginator.num_pages > 2 and page_obj.paginator.num_pages > page_obj.number + 1:
        doted_end = True
    doted_front = False
    if page_obj.paginator.num_pages > 2 and 1 < page_obj.number - 1:
        doted_front = True
    return HttpResponse(template.render(dict({
        **context,
        'pag': page_obj,
        'pages': pages,
        'url_s': url_s,
        'category': cat_items,
        'doted_end': doted_end,
        'doted_front': doted_front,
        'order': ord,
        'pod_category': pod_cat,
        'left_menu': left_menu,
        'first_pages': first_pages,
        'items': items,
        'templated_h1': templated_h1,
        'templated_title': templated_title,
        'templated_content': templated_content,
        'templated_keywords': templated_keywords,
        'templated_description': templated_description
    })))

def catalog(request):
    context, template = render_textpage(request, 'catalog', TextPage)
    if request.GET.get('sort') == 'desc':
        ordering = '-price'
        ord = 'desc'
        url_s = '?sort={}'.format(ord)
    else:
        ord = 'asc'
        ordering = 'price'
        url_s = '?sort={}'.format(ord)
    items = Item.objects.select_related('cat_item', 'pod_cat_item').all().order_by(ordering)
    template = loader.get_template("catalog.html")
    paginator = Paginator(items, 12)
    page = request.GET.get('page')
    pages = 1
    first_pages = 1
    count = items.count()
    try:
        page_obj = paginator.page(page)
        if count >= int(page) * 12:
            pages = int(page) * 12
            first_pages = int(pages) - 12 + 1
        else:
            pages = count
    except PageNotAnInteger:
        page_obj = paginator.page(1)
        pages = 1 * 12
        first_pages = pages - 12 + 1
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    direction_template = DirectionTemplate.objects.filter(type_template=1).first()
    templated_payload = dict()
    min_price = 0
    for item in items:
        if min_price == 0:
            min_price = item.price
        elif min_price > item.price:
            min_price = item.price
    templated_payload = {'cat': TextPage.objects.get(alias='catalog'), 'min_price': min_price}
    templated_h1 = Template(
        direction_template.seo_h1).render(Context(templated_payload))
    templated_title = Template(
        direction_template.seo_title).render(Context(templated_payload))
    templated_description = Template(
        direction_template.seo_description).render(Context(templated_payload))
    templated_content = Template(
        direction_template.content).render(Context(templated_payload))
    templated_keywords = Template(
        direction_template.seo_keywords).render(Context(templated_payload))

    doted_end = False
    if page_obj.paginator.num_pages > 2 and page_obj.paginator.num_pages > page_obj.number+1:
        doted_end = True
    doted_front = False
    if page_obj.paginator.num_pages > 2 and 1 < page_obj.number-1:
        doted_front = True
    return HttpResponse(template.render(dict({
        **context,
        'pag': page_obj,
        'order': ord,
        'doted_end': doted_end,
        'doted_front': doted_front,
        'url_s': url_s,
        'pages': pages,
        'first_pages': first_pages,
        'items': items,
        'templated_h1': templated_h1,
        'templated_title': templated_title,
        'templated_content': templated_content,
        'templated_keywords': templated_keywords,
        'templated_description': templated_description
    })))


def robots(request):
    template = loader.get_template('robots.txt')
    context = Robots.objects.first()
    data = {'context': context}
    return HttpResponse(template.render(data), content_type="text/plain")

def search(request):
    context, template = render_textpage(request, 'catalog', TextPage)
    url_s = '?search={}'.format(request.GET.get('search'))
    if request.GET.get('sort') == 'desc':
        ordering = '-price'
        ord = 'desc'
        url_s += '&sort={}'.format(ord)
    else:
        ord = 'asc'
        ordering = 'price'
        url_s += '&sort={}'.format(ord)
    items = Item.objects.filter(name__icontains=request.GET.get('search')).select_related('cat_item', 'pod_cat_item').all().order_by(ordering)
    template = loader.get_template("catalog.html")
    paginator = Paginator(items, 12)
    page = request.GET.get('page')
    pages = 1
    first_pages = 1
    count = items.count()
    try:
        page_obj = paginator.page(page)
        if count >= int(page) * 12:
            pages = int(page) * 12
            first_pages = int(pages) - 12 + 1
        else:
            pages = count
    except PageNotAnInteger:
        page_obj = paginator.page(1)
        pages = 1 * 12
        first_pages = pages - 12 + 1
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    doted_end = False
    if page_obj.paginator.num_pages > 2 and page_obj.paginator.num_pages > page_obj.number + 1:
        doted_end = True
    doted_front = False
    if page_obj.paginator.num_pages > 2 and 1 < page_obj.number - 1:
        doted_front = True
    return HttpResponse(template.render(dict({
        **context,
        'pag': page_obj,
        'url_s': url_s,
        'doted_end': doted_end,
        'doted_front': doted_front,
        'search': request.GET.get('search'),
        'order': ord,
        'pages': pages,
        'first_pages': first_pages,
        'items': items
    })))


@csrf_exempt
def ajax(request):
    result = {'status': 'error'}
    if request.POST['type'] == 'send_call':
        try:
            text = 'Запрос на обратный звонок. Номер телефона: {phone}'.format(phone=request.POST['phone'])
            result = send_message(text, 'main')
        except Exception as e:
            result = {'status': 'error'}
    if request.POST['type'] == 'send_call_obr':
        try:
            text = 'Заказ оптового прайса. На имя: {name}, Номер телефона: {phone}, E-mail:{email}'.format(phone=request.POST['phone'],name=request.POST['name'],email=request.POST['email'])
            result = send_message(text, 'main')
        except Exception as e:
            result = {'status': 'error'}
    if request.POST['type'] == 'send_contact_form':
        try:
            text = 'Поступил комментарий от {name} почта для связи {mail}. Комментарий: {comment}'.format(name=request.POST['name'], mail=request.POST['mail'], comment=request.POST['comment'])
            result = send_message(text, 'main')
        except Exception as e:
            result = {'status': 'error'}
    if request.POST['type'] == 'create_order':
        try:
            item = Item.objects.get(id=request.POST['product'])
            text = 'Поступил заказ на товар {item} на площадь {s} телефон для связи {phone}'.format(item=item.name, s=request.POST['s'], phone=request.POST['phone'])
            result = send_message(text, 'main')
        except Exception as e:
            result = {'status': 'error'}
    if request.POST['type'] == 'check_price':
        try:
            text = 'Поступил заказ на расчет стоимости. область применения: {first}, планируемая площадь: {second}, город: {city}, имя: {name}, телефон: {phone}, комментарий: {comment}'.format(first=request.POST['first'], second=request.POST['second'], city=request.POST['city'], name=request.POST['name'], phone=request.POST['phone'], comment=request.POST['comment'])
            result = send_message(text, 'main')
        except Exception as e:
            result = {'status': 'error'}
    return JsonResponse(result)
