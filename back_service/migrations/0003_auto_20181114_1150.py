# Generated by Django 2.1.2 on 2018-11-14 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('back_service', '0002_auto_20181113_2111'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client_ip_mac',
            old_name='ip',
            new_name='client_ip',
        ),
        migrations.RenameField(
            model_name='client_ip_mac',
            old_name='mac',
            new_name='client_mac',
        ),
    ]
