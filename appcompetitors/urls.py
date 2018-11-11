from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='appcompetitors-home'),
    path('guitars/', views.guitars, name='appcompetitors-guitars')
]
