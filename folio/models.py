from django.db import models
from django.contrib.auth.models import User

class MoexIndexData(models.Model):
    index_id = models.CharField(max_length=50)
    trade_date = models.DateField()
    ticker = models.CharField(max_length=50)
    short_name = models.CharField(max_length=255)
    sec_id = models.CharField(max_length=50)
    weight = models.FloatField()
    trading_session = models.IntegerField()

    def __str__(self):
        return f"{self.index_id} - {self.ticker} ({self.trade_date})"

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
