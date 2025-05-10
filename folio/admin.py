from django.contrib import admin
from .models import Folio

@admin.register(Folio)
class FolioAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('user', 'created_at')
    ordering = ('-created_at',)
