import random

from django.utils import timezone

# from MainScreen.receipts_jobs import create_receipt, create_receipt_invoice
from MainScreen.models import Ledger, Accounts, ReceiptsInvoice, AccountRecords, Receipts, Sitewide


def get_financial_year():
    financial_year = Sitewide.objects.latest('financial_id')
    return financial_year.financial_term_code


def due_payment_receipt_record_create(due_id, amount, member, family, account_serial, login_user, txn_remarks):
    txn_type = 'PAID'
    date = timezone.now().date()
    txn = ledger_record_create(due_id, txn_type, -amount, member, family, txn_remarks, account_serial, login_user)

    try:
        last_auto_id = Receipts.objects.latest("receipt_auto_id").receipt_auto_id
        print(last_auto_id)
        receipt_id = get_financial_year() + '-R-' + str(last_auto_id + 1)
        Receipts.objects.create(receipt_id=receipt_id, receipt_auto_id=last_auto_id + 1,
                                receipt_due_id=due_id, receipt_member=member,
                                receipt_date=date, receipt_family=family,
                                receipt_amount=amount, receipt_financial_year=get_financial_year(),
                                account_serial=account_serial, txn_id=txn, login_user=login_user,is_active=True)

    except:
        receipt_id = get_financial_year() + '-R-' + str(1)
        Receipts.objects.create(receipt_id=receipt_id, receipt_auto_id=1,
                                receipt_due_id=due_id, receipt_member=member,
                                receipt_date=date, receipt_family=family,
                                receipt_amount=amount, receipt_financial_year=get_financial_year(),
                                account_serial=account_serial,txn_id=txn,
                                login_user=login_user,is_active=True)
    #
    # receipt_id = create_receipt(due_id, member, date, family, amount, get_financial_year(),account_serial, txn, login_user)

    accountaccess = Accounts.objects.get(account_serial=account_serial,
                                         financial_year=get_financial_year())

    accountaccess.current_balance += amount
    accountaccess.cash_in_hand += amount
    accountaccess.save()
    receipt_ids = receipt_id + '/'

    AccountRecords.objects.create(account_serial=account_serial,
                                  financial_year=get_financial_year(),
                                  type="DUEPAYMENT", add_to_cash_in_hand=amount,
                                  add_to_cash_in_bank=0,
                                  add_to_current_balance=amount, txn_time=timezone.now(),
                                  txn_ref_id=receipt_id,
                                  login_user=login_user)
    return (receipt_id)


def receipt_invoice_record_create(receipt_ids, total_amount, family, login_user, txn_remarks="No Remarks"):
    try:
        last_auto_id = ReceiptsInvoice.objects.latest("receipt_invoice_auto_id").receipt_invoice_auto_id
        invoice_id = 'R/' + get_financial_year() + '/' + str(last_auto_id + 1)
        ReceiptsInvoice.objects.create(receipt_invoice_id=invoice_id, receipt_invoice_auto_id=last_auto_id + 1,
                                       receipt_financial_year=get_financial_year(), receipt_ids=receipt_ids,
                                       receipt_date=timezone.now(), login_user=login_user,
                                       total_amount=total_amount, family_no=family, is_active=True, remarks=txn_remarks)
    except:
        invoice_id = 'R/' + get_financial_year() + '/' + str(1)
        ReceiptsInvoice.objects.create(receipt_invoice_id=invoice_id, receipt_invoice_auto_id=1,
                                       receipt_financial_year=get_financial_year(), receipt_ids=receipt_ids,
                                       receipt_date=timezone.now(), login_user=login_user,
                                       total_amount=total_amount, family_no=family, is_active=True, remarks=txn_remarks)

    # create_receipt_invoice(receipt_ids,total_amount,family,login_user,get_financial_year(),timezone.now(),txn_remarks)


def ledger_record_create(due_id, txn_type, amount, member, family, txn_remarks, account_serial, login_user):
    date = timezone.now()
    try:
        last_auto_id = Ledger.objects.latest("txn_auto_id").txn_auto_id
        txn_id = 'TXN #' + str(last_auto_id + 1)
        Ledger.objects.create(txn_id=txn_id, txn_auto_id=last_auto_id + 1, txn_due_id=due_id,
                              txn_type=txn_type, txn_amount=amount,
                              txn_member=member, txn_family=family, txn_date=date,
                              txn_remarks=txn_remarks, txn_financial_year=get_financial_year(),
                              account_serial=account_serial,
                              login_user=login_user)
    except Exception:
        txn_id = 'TXN #' + str(1)
        Ledger.objects.create(txn_id=txn_id, txn_auto_id=1, txn_due_id=due_id, txn_type=txn_type,
                              txn_amount=amount, txn_member=member, txn_family=family, txn_date=date,
                              txn_remarks=txn_remarks, txn_financial_year=get_financial_year(),
                              account_serial=account_serial,
                              login_user=login_user)
    return (txn_id)
