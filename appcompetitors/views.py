from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Guitar
from .forms import UploadCSVForm
from .lib.tools import add_csv_to_db, generate_plots, generate_stats


def index(request):
    context = {
        'title': 'Home'
    }
    return render(request, 'appcompetitors/index.html', context)


def guitars(request):
    guitar_list = Guitar.objects.select_related().all()
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


def plots(request):
    chart_config = generate_plots()
    context = {
        'title': 'Plots',
        'chart_config': chart_config,
    }
    return render(request, 'appcompetitors/plots.html', context)


def stats(request):
    subbrand_list = generate_stats()
    for sb in subbrand_list: # format price
        sb['median'] = f"{sb['median']:,.2f}".replace(',', ' ')
        sb['mean'] = f"{sb['mean']:,.2f}".replace(',', ' ')
        sb['std'] = f"{sb['std']:,.2f}".replace(',', ' ')
        sb['skew'] = f"{sb['skew']:,.3f}".replace(',', ' ')
        sb['kurt'] = f"{sb['kurt']:,.3f}".replace(',', ' ')
        sb['min'] = f"{sb['min']:,.2f}".replace(',', ' ')
        sb['max'] = f"{sb['max']:,.2f}".replace(',', ' ')
        sb['range'] = f"{sb['range']:,.2f}".replace(',', ' ')
        sb['IQR'] = f"{sb['IQR']:,.2f}".replace(',', ' ')
    context = {
        'title': 'Desciptive Stats',
        'subbrand_list': subbrand_list,
    }
    return render(request, 'appcompetitors/stats.html', context)


@user_passes_test(lambda u: u.is_superuser)
def upload_csv(request):
    context = {}
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File is not CSV type')
                return redirect('competitors:guitars')
            if csv_file.multiple_chunks():
                messages.error(
                    request,
                    f'Uploaded file is too big ({csv_file.size/(1e6):.2f} MB).'
                )
                return redirect('competitors:guitars')
            entries_added = add_csv_to_db(csv_file)
            context['entries_added'] = entries_added
    else:
        form = UploadCSVForm()

    context['title'] = 'Upload CSV'
    context['form'] = form

    return render(request, 'appcompetitors/uploadcsv.html', context)
