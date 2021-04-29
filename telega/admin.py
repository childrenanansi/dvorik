from django.contrib import admin
from telega.models import *

@admin.register(Telegram)
class TelegramAdmin(admin.ModelAdmin):
    fieldsets = [("Основные", {"fields": ["url", "token", "chanel_id", "who"]})]
    list_display = ["who"]
