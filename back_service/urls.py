from django.urls import path

from . import views

urlpatterns = [
    path('request', views.request_server, name='request handler'),
    path('notify', views.notify_connection, name='notify connection'),
]
