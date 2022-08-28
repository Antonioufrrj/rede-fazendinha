from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from djgeojson.views import GeoJSONLayerView
from .models import InfoSensores, InfoDados
import datetime
import pandas as pd
import csv

class InfoSensoresGeojson(GeoJSONLayerView):
    model = InfoSensores
    properties = ('popup_content',)

'''
def InfoDadosJson(request):
    dados = InfoDados.objects.filter(sensor = 'S9').values()
    context = {
        'dados': dados
    }
    return render(request, 'core/dashboard.html', context)

def InfoDadosJson(request):
    dados = serializers.serialize('json', InfoDados.objects.filter(sensor = 'S3'))
    
    return JsonResponse(dados, safe = False)
    
    
'''

class dados(View):

    def get(self, request, nome):
        dados = InfoDados.objects.filter(sensor = nome).values()
        df = pd.DataFrame(dados)
        data = df['data'].astype(str).tolist()
        umidade = df['umidade'].tolist()
        context = {
            'nome': nome,
            'dados': dados,
            'data': data,
            'umidade': umidade
        }

        return render(request, 'core/dashboard.html', context)

def InfoDadosJson(request):
    dados = InfoDados.objects.all().values()
    context = {
        'dados': dados
    }
    return render(request, 'core/tables.html', context)

def export_csv(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dados_sensor"' + str(datetime.datetime.now().strftime('%Y-%m-%d')) + '.csv'
    writer = csv.writer(response)
    writer.writerow(['Nome do Sensor', 'Data', 'Hora', 'Capacitância', 'Umidade', 'Precipitação'])
    dados = InfoDados.objects.all()
    #print(type(dados))

    for dado in dados:
       writer.writerow([dado.sensor, dado.data, dado.hora, dado.capacitancia, dado.umidade, dado.precipitacao])

    return response