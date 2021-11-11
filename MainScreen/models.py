from django.db import models


class Members(models.Model):
    serial = models.BigAutoField(primary_key=True)
    financial_year_serial = models.TextField()
    family_number = models.IntegerField()
    family_name = models.TextField()
    member_number = models.DecimalField(decimal_places=3, max_digits=1000)
    name_eng = models.TextField()
    is_active = models.BooleanField()
    is_head = models.BooleanField()
    is_due_apply = models.BooleanField()
    is_retired = models.BooleanField()
    is_nonresident = models.BooleanField()
    is_govt = models.BooleanField()
    is_male = models.BooleanField()
    is_alive = models.BooleanField()
    age = models.IntegerField()
    area = models.TextField()
    address = models.TextField(null=True)
    postbox = models.TextField(null=True)
    mobile = models.BigIntegerField(null=True)
    email = models.TextField(null=True)
    description = models.TextField(null=True)
    remarks = models.TextField(null=True)

    class Meta:
        managed = True
        db_table = 'members'
        ordering = ['serial']


class Dues(models.Model):
    due_id = models.BigAutoField(primary_key=True)
    due_display_id = models.TextField()
    due_financial_year = models.TextField()
    due_type = models.TextField()
    due_amount = models.DecimalField(decimal_places=2, max_digits=1000)
    due_fineamt = models.DecimalField(decimal_places=2, max_digits=1000)
    is_head = models.IntegerField()
    is_retired = models.IntegerField()
    is_nonresident = models.IntegerField()
    is_govt = models.IntegerField()
    is_male = models.IntegerField()
    due_active = models.IntegerField()
    account_serial = models.TextField()
    applied = models.BooleanField()
    paid_together=models.BooleanField()

    class Meta:
        managed = True
        db_table = 'dues'


class Receipts(models.Model):
    receipt_id = models.TextField(primary_key=True)
    receipt_auto_id = models.IntegerField()
    receipt_financial_year = models.TextField()
    receipt_due_id = models.TextField()
    receipt_member = models.DecimalField(decimal_places=2, max_digits=1000)
    receipt_family = models.IntegerField()
    receipt_date = models.DateTimeField()
    receipt_amount = models.DecimalField(decimal_places=2, max_digits=1000)
    account_serial = models.TextField()
    login_user = models.TextField()
    txn_id = models.TextField()
    is_active=models.BooleanField()

    class Meta:
        managed = True
        db_table = 'receipts'


class Ledger(models.Model):
    txn_id = models.TextField(primary_key=True)
    txn_auto_id =models.IntegerField()
    txn_financial_year = models.TextField()
    txn_type = models.TextField()
    txn_due_id = models.TextField()
    txn_amount = models.DecimalField(decimal_places=2, max_digits=1000)
    txn_member = models.DecimalField(decimal_places=2, max_digits=1000)
    txn_family = models.IntegerField()
    txn_date = models.DateTimeField()
    txn_remarks = models.TextField()
    account_serial = models.TextField()
    login_user = models.TextField()

    class Meta:
        managed = True
        db_table = 'ledger'


class Sitewide(models.Model):
    financial_id = models.IntegerField(primary_key=True)
    financial_term_code = models.TextField()
    financial_year = models.TextField()
    year_start_date = models.DateField()
    year_end_date = models.DateField(null=False)
    description = models.TextField(null=False, default='2019-07-23')

    class Meta:
        managed = True
        db_table = 'sitewide'


class Accounts(models.Model):
    account_serial = models.BigAutoField(primary_key=True)
    financial_year = models.TextField()
    account_name = models.TextField()
    account_number = models.TextField()
    bank_name = models.TextField()
    is_active = models.BooleanField()
    opening_balance = models.DecimalField(max_digits=1000, decimal_places=2)
    closing_balance = models.DecimalField(max_digits=1000, decimal_places=2, null=True)
    current_balance = models.DecimalField(max_digits=1000, decimal_places=2)
    cash_in_hand = models.DecimalField(max_digits=1000, decimal_places=2)
    cash_in_bank = models.DecimalField(max_digits=1000, decimal_places=2)
    description = models.TextField(null=True)

    class Meta:
        managed = True
        db_table = 'accountsfinance'


class AccountTransactionRecords(models.Model):
    txn_id = models.BigAutoField(primary_key=True)
    account_serial = models.TextField()
    financial_year = models.TextField()
    account_name = models.TextField()
    account_number = models.TextField()
    bank_name = models.TextField()
    type = models.TextField()
    amount = models.DecimalField(max_digits=1000, decimal_places=2)
    description = models.TextField(null=True)
    txn_time = models.DateTimeField()
    login_user = models.TextField()

    class Meta:
        managed = True
        db_table = 'accountstransactionrecords'



class AccountRecords(models.Model):
    txn_id = models.BigAutoField(primary_key=True)
    account_serial = models.TextField()
    financial_year = models.TextField()
    type = models.TextField()
    add_to_cash_in_hand = models.DecimalField(max_digits=1000, decimal_places=2)
    add_to_cash_in_bank = models.DecimalField(max_digits=1000, decimal_places=2)
    add_to_current_balance = models.DecimalField(max_digits=1000, decimal_places=2)
    txn_time = models.DateTimeField()
    txn_ref_id = models.TextField()
    login_user = models.TextField()

    class Meta:
        managed = True
        db_table = 'accountsrecords'



class ReceiptsInvoice(models.Model):
    receipt_invoice_id = models.TextField(primary_key=True)
    receipt_invoice_auto_id = models.IntegerField()
    receipt_financial_year = models.TextField()
    family_no = models.IntegerField()
    receipt_ids = models.TextField()
    receipt_date = models.DateTimeField()
    login_user = models.TextField()
    total_amount = models.DecimalField(max_digits=1000, decimal_places=2)
    is_active=models.BooleanField()
    remarks= models.TextField()

    class Meta:
        managed = True
        db_table = "receiptsinvoice"

class MemberFamilyChanges(models.Model):
    id=models.AutoField(primary_key=True)
    serial=models.TextField()
    old_family=models.DecimalField(max_digits=1000, decimal_places=2)
    new_family=models.DecimalField(max_digits=1000, decimal_places=2)

    class Meta:
        managed = True
        db_table = "memberfamilychanges"
