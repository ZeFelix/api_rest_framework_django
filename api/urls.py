from django.urls import path,re_path
from .views import *

urlpatterns = [
    path('vagas',VagaList.as_view()),
    re_path('vagas/(?P<pk>[0-9])',VagaDetalhes.as_view()),
]