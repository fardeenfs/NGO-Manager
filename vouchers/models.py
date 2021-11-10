from django.db import models


class VoucherTypes(models.Model):
    serial = models.TextField(primary_key=True)
    financial_year_serial = models.TextField()
    account_serial = models.TextField()
    voucher_head = models.TextField()
    voucher_subhead = models.TextField()
    type = models.TextField()
    is_active = models.BooleanField()
    description = models.TextField()

    class Meta:
        managed = True
        db_table = 'voucher_types'


class Vouchers(models.Model):
    voucher_id = models.AutoField(primary_key=True)
    voucher_auto_id = models.IntegerField()
    voucher_display_id=models.TextField()
    voucher_financial_year = models.TextField()
    voucher_reference_id = models.TextField()
    voucher_type = models.TextField()
    voucher_amount = models.DecimalField(decimal_places=2, max_digits=1000)
    remarks = models.TextField()
    voucher_head = models.TextField()
    voucher_subhead = models.TextField()
    voucher_date = models.DateTimeField(null=False)
    account_serial = models.TextField()
    voucher_member_name = models.TextField(null=False)
    voucher_member_address = models.TextField(null=False)
    login_user = models.TextField()
    is_active=models.BooleanField()


    class Meta:
        managed = True
        db_table = 'vouchers'
