import decimal

from django.shortcuts import render, redirect

from django.utils import timezone

from MainScreen.models import Sitewide, Accounts, AccountRecords
from vouchers.models import Vouchers, VoucherTypes
from django.contrib.auth.decorators import login_required


def get_financial_year():
    financial_year = Sitewide.objects.latest('financial_id')
    return financial_year.financial_term_code


@login_required
def voucher_view(request):
    vouchers = Vouchers.objects.filter(voucher_financial_year=get_financial_year(), is_active=1)
    vouchers = vouchers.order_by('-voucher_date')
    context = {}
    context["voucherhead"] = ['Record ID', 'Type ID', 'Head', 'Type', 'Amount',
                              'Date', 'Remarks', 'Print', 'Cancel']
    context["voucherrecord"] = []
    for voucher in vouchers:
        context["voucherrecord"].append([voucher.voucher_display_id, voucher.voucher_reference_id, voucher.voucher_head,
                                        voucher.voucher_type, voucher.voucher_amount, voucher.voucher_date, voucher.remarks])
    context["expensevouchertypes"] = get_new_expense_voucher()
    context["incomevouchertypes"] = get_new_income_voucher()

    if request.method == "POST":
        name = request.POST['vname']
        address = request.POST['vaddress']
        voucher_amt = decimal.Decimal(request.POST['vamt'])
        voucher_type_head = request.POST['vhead']
        vremarks = request.POST['vremarks']
        reference_type_object = VoucherTypes.objects.get(voucher_head=voucher_type_head,
                                                         type=request.POST['type'])
        reference_id = reference_type_object.serial
        reference_type = reference_type_object.type
        account_serial = reference_type_object.account_serial
        voucher_date = timezone.now()
        vouchers = Vouchers.objects.filter(voucher_type=reference_type)
        print(vouchers)
        if len(vouchers) != 0:
            lst=[]
            for v in vouchers:
                lst.append(int(v.voucher_auto_id))
            voucher_auto_id=max(lst)+1
        else:
            voucher_auto_id=1
        voucher_display_id='V/'+reference_type[:3]+'/'+str(voucher_auto_id)

        Vouchers.objects.create(voucher_display_id=voucher_display_id,
                                voucher_auto_id=voucher_auto_id,
                                voucher_financial_year=get_financial_year(),
                                voucher_reference_id=reference_id, voucher_type=reference_type,
                                voucher_amount=voucher_amt, remarks=vremarks, voucher_head=voucher_type_head,
                                voucher_date=voucher_date,
                                account_serial=account_serial,
                                voucher_member_name=name, voucher_member_address=address, is_active=1,
                                login_user=request.user.get_username())

        accountaccess = Accounts.objects.get(account_serial=account_serial, financial_year=get_financial_year())
        if reference_type == 'EXPENSE':
            accountaccess.current_balance -= voucher_amt
            accountaccess.cash_in_hand -= voucher_amt
            accountrecord = AccountRecords.objects.create(account_serial=account_serial,
                                                          financial_year=get_financial_year(),
                                                          type="EXP-VOUCHER", add_to_cash_in_hand=-voucher_amt,
                                                          add_to_cash_in_bank=0,
                                                          add_to_current_balance=-voucher_amt, txn_time=voucher_date,
                                                          txn_ref_id=voucher_display_id,
                                                          login_user=request.user.get_username())
        else:
            accountaccess.current_balance += voucher_amt
            accountaccess.cash_in_hand += voucher_amt
            accountrecord = AccountRecords.objects.create(account_serial=account_serial,
                                                          financial_year=get_financial_year(),
                                                          type="INC-VOUCHER", add_to_cash_in_hand=voucher_amt,
                                                          add_to_cash_in_bank=0,
                                                          add_to_current_balance=voucher_amt, txn_time=voucher_date,
                                                          txn_ref_id=voucher_display_id,
                                                          login_user=request.user.get_username())
        accountaccess.save()
        return redirect('/vouchers/')

    return render(request, 'voucher.html', context)


def get_new_expense_voucher():
    vouchertypes = {}
    types = VoucherTypes.objects.filter(type="EXPENSE", financial_year_serial=get_financial_year())
    for type in types:
        if type.voucher_head not in vouchertypes.keys():
            vouchertypes[type.voucher_head] = []
            vouchertypes[type.voucher_head].append(type.voucher_subhead)
        else:
            vouchertypes[type.voucher_head].append(type.voucher_subhead)
    return vouchertypes


def get_new_income_voucher():
    vouchertypes = {}
    types = VoucherTypes.objects.filter(type="INCOME", financial_year_serial=get_financial_year())
    for type in types:
        if type.voucher_head not in vouchertypes.keys():
            vouchertypes[type.voucher_head] = []
            vouchertypes[type.voucher_head].append(type.voucher_subhead)
        else:
            vouchertypes[type.voucher_head].append(type.voucher_subhead)
    return vouchertypes


@login_required()
def printvoucher(request):
    if request.method == "GET":
        data = {}
        voucher = request.GET["voucher-id"]
        rec = Vouchers.objects.get(voucher_display_id=voucher)
        data["invoice"] = {
            "name": rec.voucher_member_name,
            "voucher_no": voucher,
            "type": rec.voucher_type,
            "date": rec.voucher_date,
            "address": rec.voucher_member_address,
            "recs": [[rec.voucher_head, rec.voucher_subhead, rec.voucher_amount]],
            "total": rec.voucher_amount,
            "remarks": rec.remarks
        }
        return render(request, 'voucher-print.html', data)


def cancelvoucher(request):
    voucher_id = request.POST['voucher-id']
    voucher = Vouchers.objects.get(voucher_display_id=voucher_id)
    accountaccess = Accounts.objects.get(account_serial=voucher.account_serial, financial_year=get_financial_year())
    if voucher.voucher_type == 'INCOME':
        accountaccess.current_balance -= voucher.voucher_amount
        accountaccess.cash_in_hand -= voucher.voucher_amount
        accountrecord = AccountRecords.objects.get(txn_ref_id=voucher_id, type="INC-VOUCHER")
    else:
        accountaccess.current_balance += voucher.voucher_amount
        accountaccess.cash_in_hand += voucher.voucher_amount
        accountrecord = AccountRecords.objects.get(txn_ref_id=voucher_id, type="EXP-VOUCHER")
    accountaccess.save()
    voucher.delete()
    accountrecord.delete()
    return redirect('/vouchers')
