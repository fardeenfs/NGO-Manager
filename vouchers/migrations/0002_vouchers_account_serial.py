# Generated by Django 3.2.4 on 2021-07-14 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vouchers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vouchers',
            name='account_serial',
            field=models.TextField(default='AC-1'),
            preserve_default=False,
        ),
    ]
