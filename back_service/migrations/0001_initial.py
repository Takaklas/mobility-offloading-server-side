# Generated by Django 2.1.2 on 2018-11-13 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='client_ip_mac',
            fields=[
                ('mac', models.CharField(blank=True, editable=False, max_length=20, primary_key=True, serialize=False)),
                ('ip', models.GenericIPAddressField(protocol='IPv4')),
            ],
        ),
    ]
