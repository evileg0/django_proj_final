from django.db import models
from django.contrib.auth.models import User

class MoexIndexData(models.Model):
    index_id = models.CharField(max_length=50)
    trade_date = models.DateField()
    ticker = models.CharField(max_length=50, verbose_name='Тикер')
    short_name = models.CharField(max_length=255, verbose_name='Краткое название')
    sec_id = models.CharField(max_length=50)
    weight = models.FloatField(verbose_name='Вес в индексе')
    trading_session = models.IntegerField()

    def __str__(self):
        return f"{self.index_id} - {self.ticker} ({self.trade_date})"

    class Meta:
        verbose_name = 'Ценная бумага в индексе (MOEX)'
        verbose_name_plural = 'Ценные бумаги в индексе (MOEX)'

class SecuritiesIndexData(models.Model):
    secid = models.CharField(max_length=50, verbose_name='Тикер', unique=True)
    shortname = models.CharField(max_length=255, verbose_name='Краткое название')
    prevprice = models.FloatField(verbose_name='Предыдущая цена')
    lotsize = models.IntegerField(verbose_name='Размер лота')

    def __str__(self):
        return f"{self.secid} — {self.shortname}"

    class Meta:
        verbose_name = 'Ценная бумага (MOEX)'
        verbose_name_plural = 'Ценные бумаги (MOEX)'

class Folio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Портфель'
        verbose_name_plural = 'Портфели'
