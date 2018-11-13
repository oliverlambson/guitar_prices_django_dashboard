import csv
import codecs

from django.utils import timezone
from django.contrib import messages

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
    pass
