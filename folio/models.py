from django.db import models

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
