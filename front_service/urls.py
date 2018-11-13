from django.urls import path

from . import views

urlpatterns = [
    path('request', views.request_server, name='request handler'),
    path('', views.index, name='index'),
]
