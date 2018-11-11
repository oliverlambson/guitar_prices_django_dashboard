from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SubBrand(models.Model):
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Range(models.Model):
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Model(models.Model):
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Guitar(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    subbrand = models.ForeignKey(SubBrand, on_delete=models.CASCADE)
    rnge = models.ForeignKey(Range, on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    variant = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=11, decimal_places=2)
    source = models.URLField()
    date_added = models.DateTimeField()
    date_updated = models.DateTimeField()

    def __str__(self):
        return (
            f'{self.brand.name} {self.subbrand.name} {self.rnge.name}'
            f' {self.model.name} {self.variant}'
        )
