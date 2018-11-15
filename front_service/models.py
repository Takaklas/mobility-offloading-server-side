from django.db import models

# Create your models here.

class Client_ip_mac(models.Model):
    client_mac = models.CharField(primary_key=True,max_length=20,editable=False)
    client_ip = models.GenericIPAddressField(protocol='IPv4') #(protocol='both')
