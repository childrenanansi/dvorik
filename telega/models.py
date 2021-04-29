from django.db import models

class Telegram(models.Model):
    class Meta:
        verbose_name = u"Данные от телеграм бота"
        verbose_name_plural = u"Данные от телеграм бота"

    url = models.CharField(max_length=200, verbose_name=u"URL", default='https://api.telegram.org/bot', null=True, blank=True)
    token = models.CharField(max_length=200, verbose_name=u"TOKEN", null=True, blank=True)
    chanel_id = models.CharField(max_length=200, verbose_name=u"Название канала или id", null=True, blank=True)
    who = models.CharField(max_length=200, verbose_name=u"ID назначения", null=True, blank=True, default='main')

    def __str__(self):
        return self.who