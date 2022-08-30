from django.shortcuts import render
from infosensor.models import InfoDados

def index(request):
    return render(request, 'core/index.html')

def mapa(request):
    return render(request, 'core/mapa.html')

def dashboard(request):
    return render(request, 'core/dashboard.html')

