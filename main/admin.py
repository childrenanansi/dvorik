from django.contrib import admin
from main.models import *

page_fields = [(u"Настройки страницы", {
    "fields": ["menutitle", "canonical", "alias", "menushow", "menuposition", "sitemap"]
}),
    (u"Open Graph", {
        "fields": [
            "og_title", "og_description", "og_type_pb_time",
            "og_type_author"
        ]
    }),
    (u"SEO информация", {
        "fields": [
            "seo_h1",
            "seo_title",
            "seo_description",
            "seo_keywords",
            "content",
        ]
    })]
page_list = ("menushow", "sitemap")

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    fieldsets = [("Основные", {"fields": ["robots", "phone", "address", "header_additional", "metrics_google", "metrics_yandex"]})]

class Banner(admin.TabularInline):
    model = Banner

class Akcii(admin.TabularInline):
    model = Akcii

@admin.register(TextPage)
class TextPageAdmin(admin.ModelAdmin):
    fieldsets = [("Основные", {"fields": ["name", "is_service", "img_path"]})] + page_fields
    list_display = ["name", "is_service"]
    inlines = [
        Banner, Akcii
    ]

@admin.register(DirectionTemplate)
class DirectionTemplateAdmin(admin.ModelAdmin):
    fieldsets = [("Основные", {"fields": ["name", "type_template"]})] + page_fields
    list_display = ["name"]


@admin.register(CatProject)
class CatProject(admin.ModelAdmin):
    fieldsets = [("Основные", {"fields": ["name"]})] + page_fields
    list_display = ["name", "menuposition"]
    list_editable = ['menuposition']


class SliderInline(admin.TabularInline):
    model = Slider

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    fieldsets = [("Основные", {"fields": ["name", "cat", "img_front"]})] + page_fields
    list_display = ["name"]
    inlines = [
        SliderInline,
    ]

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    fieldsets = [("Основные", {"fields": ["name", "image", "display_home", 'project']})]
    list_display = ["name"]

@admin.register(CatItems)
class CatItemsAdmin(admin.ModelAdmin):
    fieldsets = [("Основные", {"fields": ["name", "img_front", "ico"]})] + page_fields
    list_display = ["name", "menuposition"]
    list_editable = ['menuposition']

@admin.register(PodCatItems)
class PodCatItemsAdmin(admin.ModelAdmin):
    fieldsets = [("Основные", {"fields": ["name", "img_front", "ico", "parent"]})] + page_fields
    list_display = ["name", "menuposition"]
    list_editable = ['menuposition']

class ImgInline(admin.TabularInline):
    model = Img
    exclude = ("menutitle", "canonical", "alias", "menushow", "menuposition", "sitemap","og_title", "og_description", "og_type_pb_time",
            "og_type_author", "seo_h1",
            "seo_title",
            "seo_description",
            "seo_keywords",
            "content",)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "price_kv", "price_for_wt", "size", "dlina", "obrob", "des_right", "published", "show_on_index", 'img_front', 'label_new', 'label_hit', 'cat_item', 'pod_cat_item']
    list_filter = ["name"]
    list_editable = ['price', 'price_kv']
    inlines = [
        ImgInline,
    ]

@admin.register(Img)
class ImgAdmin(admin.ModelAdmin):
    fieldsets = [("Основные", {"fields": ["name", "img", "item"]})] + page_fields
    list_display = ["item", "name", "img"]

@admin.register(Robots)
class RobotsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Содержимое', {
            'fields': ['content']
        }),
    ]

@admin.register(Crosssell)
class CrosssellAdmin(admin.ModelAdmin):
    fieldsets = [("Основные", {"fields": ["item", "cross"]})]
    list_filter = ["item__name"]

@admin.register(Upsell)
class UpsellAdmin(admin.ModelAdmin):
    fieldsets = [("Основные", {"fields": ["item", "ups"]})]
    list_filter = ["item__name"]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["name", "item", "telephone", "email", "text"]
    list_filter = ["item__name"]