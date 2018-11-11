# Generated by Django 2.1.3 on 2018-11-11 07:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Guitar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variant', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=11)),
                ('source', models.URLField()),
                ('date_added', models.DateTimeField()),
                ('date_updated', models.DateTimeField()),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appcompetitors.Brand')),
            ],
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appcompetitors.Brand')),
            ],
        ),
        migrations.CreateModel(
            name='Range',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appcompetitors.Brand')),
            ],
        ),
        migrations.CreateModel(
            name='SubBrand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appcompetitors.Brand')),
            ],
        ),
        migrations.AddField(
            model_name='guitar',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appcompetitors.Model'),
        ),
        migrations.AddField(
            model_name='guitar',
            name='rnge',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appcompetitors.Range'),
        ),
        migrations.AddField(
            model_name='guitar',
            name='subbrand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appcompetitors.SubBrand'),
        ),
    ]