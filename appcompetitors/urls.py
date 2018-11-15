from django.urls import path

from . import views

app_name = 'competitors'

urlpatterns = [
    path('', views.index, name='home'),
    path('guitars/', views.guitars, name='guitars'),
    path('upload_csv/', views.upload_csv, name='upload_csv'),
    path('plots/', views.plots, name='plots'),
    path('stats/', views.stats, name='stats'),
]
