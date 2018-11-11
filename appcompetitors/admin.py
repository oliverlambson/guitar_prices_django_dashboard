from django.contrib import admin

from .models import Brand, SubBrand, Range, Model, Guitar

admin.site.register(Brand)
admin.site.register(SubBrand)
admin.site.register(Range)
admin.site.register(Model)
admin.site.register(Guitar)
