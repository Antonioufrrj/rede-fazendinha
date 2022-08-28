from django.urls import path, include
from . import views as v

app_name = 'infosensor'

urlpatterns = [

    path('geojson/', v.InfoSensoresGeojson.as_view(), name='infosensores_geojson'),
    path('json:<str:nome>/', v.dados.as_view(), name='infodados_json'),
    path('tables/', v.InfoDadosJson, name='infodados'),
    path('export_csv', v.export_csv, name='export-csv')
]