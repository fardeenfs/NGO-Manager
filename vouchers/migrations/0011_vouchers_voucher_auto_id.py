# Generated by Django 3.2.4 on 2021-08-15 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vouchers', '0010_alter_vouchers_voucher_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='vouchers',
            name='voucher_auto_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]