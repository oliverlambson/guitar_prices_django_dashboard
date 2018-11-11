from django.shortcuts import render
from django.http import HttpResponse

from .models import Guitar


def index(request):
    context = {
        'title': 'Home'
    }
    return render(request, 'appcompetitors/index.html', context)


def guitars(request):
    guitar_list = Guitar.objects.all()
    for guitar in guitar_list: # format price
        guitar.price = f'{guitar.price:,.2f}'.replace(',', ' ')

    context = {
        'title': 'Guitars',
        'guitar_list': guitar_list
    }
    return render(request, 'appcompetitors/guitars.html', context)
