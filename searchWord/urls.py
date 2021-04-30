from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('wod', views.wod, name="wod"),
    path('word', views.word, name='word'),
    path('pod', views.pod, name="pod")
]