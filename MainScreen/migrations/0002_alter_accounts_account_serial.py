# Generated by Django 3.2.4 on 2021-11-10 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainScreen', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounts',
            name='account_serial',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
