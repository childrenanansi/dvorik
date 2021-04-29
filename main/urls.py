from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import handler404, handler500
from . import views

app_name = 'main'

handler404 = views.page_404

#sitemaps = {
#    'textpage': views.TextPageSitemap,
#    'category': views.CategorySitemap,
#    'subcategory': views.SubcategorySitemap,
#    'item': views.ItemSitemap,
#}


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'index/', views.index_home, name='index'),
    url(r'contact/', views.contact, name='contact'),
    url(r'delivery/', views.delivery, name='delivery'),
    url(r'optovikam/', views.optovikam, name='optovikam'),
    path('catalog/<parent>/<alias>/', views.catalog_items, name='catalog_item_item'),
    path('catalog/<alias>/', views.catalog_items, name='catalog_item'),
    path('product/<alias>/', views.product, name='product'),
    path('catalog/', views.catalog, name='catalog'),
    path('raboti/<alias>/', views.raboti_item, name='raboti_item'),
    url(r'raboti/', views.raboti, name='raboti'),
    url(r'ajax/', views.ajax, name='ajax'),
    url(r'search/', views.search, name='search'),
    path('robots.txt', views.robots),
    path('<alias>/', views.textpage, name='textpage'),
    url(r'^sitemap.xml$', views.sitemap_xml, name='sitemap_xml'),
]
