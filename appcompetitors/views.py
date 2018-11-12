from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Guitar
from .forms import UploadCSVForm
from .lib.tools import add_csv_to_db


def index(request):
    context = {
        'title': 'Home'
    }
    return render(request, 'appcompetitors/index.html', context)


def guitars(request):
    guitar_list = Guitar.objects.all()
    for guitar in guitar_list: # format price
        guitar.price = f'{guitar.price:,.2f}'.replace(',', ' ')

    page = request.GET.get('page', 1)
    paginator = Paginator(guitar_list, 10)
    try:
        guitar_list = paginator.page(page)
    except PageNotAnInteger:
        guitar_list = paginator.page(1)
    except EmptyPage:
        guitar_list = paginator.page(paginator.num_pages)

    context = {
        'title': 'Guitars',
        'guitar_list': guitar_list
    }
    return render(request, 'appcompetitors/guitars.html', context)

@user_passes_test(lambda u: u.is_superuser)
def upload_csv(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
        # if True:
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File is not CSV type')
                return HttpResponseRedirect(reverse('competitors:guitars'))
            if csv_file.multiple_chunks():
                messages.error(
                    request,
                    f'Uploaded file is too big ({csv_file.size/(1e6):.2f} MB).'
                )
                return HttpResponseRedirect(reverse('competitors:guitars'))
            add_csv_to_db(csv_file)
            return HttpResponseRedirect(reverse('competitors:guitars'))
    else:
        form = UploadCSVForm()
    context = {
        'title': 'Upload CSV',
        'form': form,
    }
    return render(request, 'appcompetitors/uploadcsv.html', context)
