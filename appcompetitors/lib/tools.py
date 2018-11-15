import csv
import codecs
import pandas as pd
import numpy as np

from django.utils import timezone
from django.contrib import messages
from django.db import connection
from django.db.models import F

from appcompetitors.models import Brand, SubBrand, Range, Model, Guitar


def add_csv_to_db(file):
    entries_added = {
        'brands': [],
        'subbrands': [],
        'ranges': [],
        'models': [],
        'guitars': []
    }
    csv_rows = csv.reader(codecs.iterdecode(file, 'utf-8'), delimiter=';')
    i = 0
    types_ok = True
    for row in csv_rows:
        (
            arg_brand,
            arg_sub_brand,
            arg_range_name,
            arg_model,
            arg_variant,
            arg_year,
            arg_price
        ) = row

        try:
            arg_year = int(arg_year)
            arg_price = float(arg_price)
        except ValueError:
            types_ok = False
            print("!! type not ok")

        if types_ok:
            brand, new_brand = Brand.objects.get_or_create(
                name=arg_brand
            )
            sub_brand, new_sub_brand = SubBrand.objects.get_or_create(
                name=arg_sub_brand,
                brand=brand
            )
            range_name, new_range = Range.objects.get_or_create(
                name=arg_range_name,
                brand=brand
            )
            model, new_model = Model.objects.get_or_create(
                name=arg_model,
                brand=brand
            )
            guitar, new_guitar = Guitar.objects.get_or_create(
                brand=brand,
                subbrand=sub_brand,
                rnge=range_name,
                model=model,
                variant=arg_variant,
                year=arg_year,
                price=arg_price,
                defaults={
                    'date_added': timezone.now(),
                    'date_updated': timezone.now()
                }
            )
            if new_brand:
                entries_added['brands'].append(brand.name)
            if new_sub_brand:
                entries_added['subbrands'].append(sub_brand.name)
            if new_range:
                entries_added['ranges'].append(range_name.name)
            if new_model:
                entries_added['models'].append(model.name)
            if new_guitar:
                entries_added['guitars'].append(
                    f"{brand.name} {sub_brand.name} "
                    f"{range_name.name} {model.name} {arg_variant} "
                    f"{arg_year} ${arg_price:.2f}"
                )

    return entries_added


def generate_plots():
    # setup chart format
    chart_config = {}
    chart_config['bindto'] = '#chart_test'
    chart_config['data'] = {
        'json': {},
        'xs': {},
        'names': {},
        'types': {},
    }
    chart_config['line'] = {
        'step': {
            'type': 'step-after'
        }
    }
    chart_config['axis'] = {
        'x': {
            'label': {},
            'tick': {},
        },
        'y': {
            'label': {},
        },
    }
    chart_config['axis']['x']['label']['text'] = 'Price (US$)'
    chart_config['axis']['x']['label']['position'] = 'outer-center'
    # chart_config['axis']['x']['tick']['fit'] = True
    chart_config['axis']['y']['label']['text'] = 'Frequency'
    chart_config['axis']['y']['label']['position'] = 'outer-middle'


    # store database in pandas dataframe
    query = str(
        Guitar.objects
        .select_related('brand', 'subbrand')
        .only('price', 'brand__name', 'subbrand__name')
        .annotate(brand_name=F('brand__name'))
        .annotate(subbrand_name=F('subbrand__name'))
        .order_by('price')
        .query
    )
    # print(query)
    df = pd.read_sql_query(query, connection)
    df.drop(columns=df.filter(like='id').columns, inplace=True)
    df.drop(columns='name', inplace=True)
    # print(df.head())

    x_tick_values = range(0,np.max(df['price'])+500,500)
    chart_config['axis']['x']['tick']['values'] = list(x_tick_values)

    # process data
    brands = sorted(df['brand_name'].unique())
    all_brands = '\n'.join(brand for brand in brands)
    all_subbrands = {}

    for i, brand in enumerate(brands):
        df_b = df.loc[df['brand_name'] == brand]
        subbrands = df_b['subbrand_name'].unique()
        all_subbrands[f'{brand}'] = list(subbrands)

        for j, subbrand in enumerate(subbrands):
            df_sb = df_b.loc[df_b['subbrand_name'] == subbrand]

            # CALCULATE HISTOGRAM
            # good source: https://realpython.com/python-histograms/
            freq, bin_edges = np.histogram(
                df_sb['price'], bins='auto', density=False
            )
            bin_size = bin_edges[1] - bin_edges[0]
            # process to plot on line/step/fill chart
                # make len(freq) == len(bin_edges)
            freq = np.append(freq, freq[-1])
                # start and end freq and bin_edges at freq of 0
            freq = np.concatenate([[0], freq, [0]])
            bin_edges = np.concatenate([[bin_edges[0]], bin_edges, [bin_edges[-1]]])

            freq = freq.astype(float) # json serializer doesn't like ints
            bin_edges = np.around(bin_edges, decimals=2) # currency format

            # write data to chart dict
            chart_config['data']['json'][f'bins_{i}.{j}'] = list(bin_edges)
            chart_config['data']['json'][f'freq_{i}.{j}'] = list(freq)
            chart_config['data']['xs'][f'freq_{i}.{j}'] = f'bins_{i}.{j}'
            chart_config['data']['names'][f'freq_{i}.{j}'] = f'{brand} {subbrand}'
            chart_config['data']['types'][f'freq_{i}.{j}'] = 'area-step'

            # # CALCULATE KDE
            # # good source: https://jakevdp.github.io/blog/2013/12/01/kernel-density-estimation/
            # kde = gaussian_kde(df_sb['Price'].values)
            # kde_val_min = np.min(df_sb['Price'].values) - bin_size/2
            # kde_val_max = np.max(df_sb['Price'].values) + bin_size/2
            # kde_vals = np.linspace(kde_val_min, kde_val_max, 100)
            # kde_prob = kde.evaluate(kde_vals)
    return chart_config
