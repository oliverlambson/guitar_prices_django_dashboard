from django.shortcuts import render
from django.http import HttpResponse

from .models import Guitar


def index(request):
    return render(request, 'appcompetitors/index.html')


def guitars(request):
    guitar_list = Guitar.objects.all()
    context = {
        'guitar_list': guitar_list
    }
    return render(request, 'appcompetitors/guitars.html', context)
