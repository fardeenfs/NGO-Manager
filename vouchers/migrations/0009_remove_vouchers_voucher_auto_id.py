# Generated by Django 3.2.4 on 2021-08-08 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vouchers', '0008_auto_20210808_1433'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vouchers',
            name='voucher_auto_id',
        ),
    ]
