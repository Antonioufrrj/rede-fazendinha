from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import InfoSensores, InfoDados

@admin.register(InfoSensores)
class InfoSensoresAdmin(LeafletGeoAdmin):
    list_display = ['nome_sensor', 'geom', 'funcao',  'cultura', 'altitude', 'profundidade', 'cap_campo',
                    'murcha_pmt', 'adt', 'comentarios']

@admin.register(InfoDados)
class InfoDadosAdmin(LeafletGeoAdmin):
    list_display = ['sensor', 'data', 'hora', 'capacitancia', 'umidade', 'precipitacao']
