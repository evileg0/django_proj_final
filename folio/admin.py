from django.contrib import admin
from .models import Folio, SecuritiesIndexData, MoexIndexData, MoexIndexData

@admin.register(Folio)
class FolioAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(SecuritiesIndexData)
class SecuritiesIndexDataAdmin(admin.ModelAdmin):
    list_display = ('secid', 'shortname', 'prevprice', 'lotsize')
    search_fields = ('secid', 'shortname')
    ordering = ('shortname',)

@admin.register(MoexIndexData)
class MoexIndexDataAdmin(admin.ModelAdmin):
    list_display = ('index_id', 'ticker', 'short_name', 'trade_date', 'weight', 'trading_session')
    search_fields = ('ticker', 'short_name', 'sec_id')
    ordering = ('ticker',)
