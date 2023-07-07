from django.contrib import admin
from .models import Conta, Categoria

"""
class ListandoFotografias(admin.ModelAdmin):
    list_display = ["id", "nome", "legenda", "publicada"]
    list_display_links = ["id", "nome"]
    search_fields = ["nome"]
    list_filter = ["categoria"]
    list_per_page = 10
    list_editable = ["publicada"]
"""

admin.site.register(Conta)
admin.site.register(Categoria)
