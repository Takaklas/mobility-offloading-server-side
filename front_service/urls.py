from django.urls import path

from . import views

urlpatterns = [
    path('request', views.request_server, name='request handler'),
    path('imageUpload', views.image_upload, name='image processing'),
    path('forward', views.forward_response, name='forward a response'),
    path('', views.index, name='index'),
]
