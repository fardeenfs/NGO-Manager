import decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from vouchers.models import Vouchers
from .forms import NewDue, NewMember, NewFamily, EditMember, EditDues
from MainScreen.models import Members, Dues, Receipts, Ledger, Sitewide, Accounts, AccountTransactionRecords, \
    ReceiptsInvoice, AccountRecords, MemberFamilyChanges

from django.contrib.auth.decorators import login_required
import random
import csv

from django.http import HttpResponse

import MainScreen.writefuncs as wf


# from .receipts_jobs import filter_receiptinvoices_by_family


def temporaryadd(request):
    AccountRecords.objects.create(account_serial='AC-1', financial_year='FM-3', type="OPENING",
                                  add_to_cash_in_hand=4431,
                                  add_to_cash_in_bank=676780, add_to_current_balance=681211, txn_time=timezone.now(),
                                  txn_ref_id="NA",
                                  login_user=request.user.get_username())
    AccountRecords.objects.create(account_serial='AC-2', financial_year='FM-3', type="OPENING", add_to_cash_in_hand=0,
                                  add_to_cash_in_bank=839268, add_to_current_balance=839268, txn_time=timezone.now(),
                                  txn_ref_id="NA",
                                  login_user=request.user.get_username())
    AccountRecords.objects.create(account_serial='AC-3', financial_year='FM-3', type="OPENING", add_to_cash_in_hand=0,
                                  add_to_cash_in_bank=1462.50, add_to_current_balance=1462.50, txn_time=timezone.now(),
                                  txn_ref_id="NA",
                                  login_user=request.user.get_username())
    AccountRecords.objects.create(account_serial='AC-4', financial_year='FM-3', type="OPENING", add_to_cash_in_hand=0,
                                  add_to_cash_in_bank=0, add_to_current_balance=0, txn_time=timezone.now(),
                                  txn_ref_id="NA",
                                  login_user=request.user.get_username())
    AccountRecords.objects.create(account_serial='AC-5', financial_year='FM-3', type="OPENING", add_to_cash_in_hand=0,
                                  add_to_cash_in_bank=94000, add_to_current_balance=94000, txn_time=timezone.now(),
                                  txn_ref_id="NA",
                                  login_user=request.user.get_username())
    AccountRecords.objects.create(account_serial='AC-6', financial_year='FM-3', type="OPENING", add_to_cash_in_hand=0,
                                  add_to_cash_in_bank=559666, add_to_current_balance=559666, txn_time=timezone.now(),
                                  txn_ref_id="NA",
                                  login_user=request.user.get_username())
    return HttpResponse('DONE')


def get_financial_year():
    financial_year = Sitewide.objects.latest('financial_id')
    return financial_year.financial_term_code


def getdata(dt_type, value, request):
    context = {}
    context = {"header": ['Member No.', 'Member Name', 'Family No.', 'Outstanding Balance']}

    # Member Search
    if dt_type == "members":
        flag = ''
        try:
            value = decimal.Decimal(value)
        except Exception:
            flag = 'string'
        # Member Search With Decimal
        if flag != 'string':
            try:
                result = Members.objects.get(member_number=value, is_active=True)
                context["rows"] = [[result.member_number.normalize(), result.name_eng, result.family_number,
                                    format(get_member_dues_balance(value), ".2f")]]
                return (context)
            except:
                pass

        # Member Search With Text
        else:
            result = Members.objects.filter(name_eng__istartswith=value.lower(), is_active=True).order_by("name_eng")
            context["rows"] = (
                [[member.member_number.normalize(), member.name_eng, member.family_number,
                  format(get_member_dues_balance(member.member_number), ".2f")] for member in result])
            return (context)


    # Family Search
    elif dt_type == "family":

        # Family Search With Decimal
        if value.isdecimal():
            context["xrows"] = {}
            context["family_data"] = {}
            col = 0
            result = Members.objects.filter(family_number=value, is_active=True).order_by("family_name")
            for member in result:
                if member.family_number in context["xrows"].keys():
                    context["xrows"][member.family_number].append(
                        [member.member_number.normalize(), member.name_eng, member.family_number,
                         format(get_member_dues_balance(member.member_number), ".2f")])
                else:
                    context["xrows"][member.family_number] = [[]]
                    context["xrows"][member.family_number][0] = (
                        member.member_number.normalize(), member.name_eng, member.family_number,
                        format(get_member_dues_balance(member.member_number), ".2f"))
                if member.is_head:
                    context["family_data"][col] = [member.family_number, member.family_name,
                                                   member.area, member.postbox]
                    col += 1

            return (context)

        # Family Search With Text
        else:
            i = 0
            context["xrows"] = {}
            context["family_data"] = {}
            raw_result = Members.objects.filter(family_name__istartswith=value, is_active=True).order_by("family_name")
            families = []
            for family in raw_result:
                if family.family_number not in families:
                    families.append(family.family_number)
            for family in families:
                result = Members.objects.filter(family_number=family)
                for member in result:
                    if family in context["xrows"].keys():
                        x = len(context["xrows"][family])
                        context["xrows"][family].append(
                            (member.member_number.normalize(), member.name_eng, member.family_number,
                             get_member_dues_balance(member.member_number)))
                    else:
                        context["xrows"][family] = [[]]
                        context["xrows"][family][0] = (
                            member.member_number.normalize(), member.name_eng, str(member.family_number),
                            get_member_dues_balance(member.member_number))
                        context["family_data"][i] = [member.family_number, member.family_name,
                                                     member.area, member.postbox]
                        i += 1
            return context

    elif dt_type == "reciept":
        return redirect('/invoice/?Receipt+No.=' + value)


@login_required()
def homeloaded(request):
    context = {}
    if request.method == 'POST':
        member = request.POST['MemberSearch']
        family = request.POST['FamilySearch']
        receipt = request.POST['ReceiptSearch']
        if member != '':
            context = getdata('members', member, request)
        elif family != '':
            context = getdata('family', family, request)
        elif receipt != '':
            context = getdata('receipt', receipt, request)
            return redirect('/invoice/?Receipt+No.=' + receipt)
        else:
            context = getdata('members', '', request)
        return render(request, 'home.html', context)
    else:
        context = getdata('members', '', request)
    return render(request, 'home.html', context)


@login_required()
def getdues(request):
    context = {}
    if request.method == "GET":
        family = request.GET['family-dues']

        # Initializing Variables To Be Used
        context['duefamily'] = []
        context['dues'] = []
        context['familyprofile'] = family
        context["familyreceipts"] = []
        context["members"] = {}

        result = Members.objects.filter(family_number=family)
        dues = Dues.objects.all()

        for member in result:
            # Fetching Family Details
            if member.is_head:
                context['duefamily'] = [member.family_number, member.family_name,
                                        member.area, member.postbox]

            # Finding Head Of Family
            if member.is_head:
                context['head'] = [member.name_eng, member.member_number.normalize(), str(member.mobile)]

            # Fetching Dues
            for due in dues:
                txns_dues = Ledger.objects.filter(txn_member__exact=member.member_number,
                                                  txn_due_id__exact=due.due_display_id,
                                                  txn_financial_year=get_financial_year())
                dues_total = 0
                for txn in txns_dues:
                    dues_total += txn.txn_amount
                if len(txns_dues) != 0:
                    if (dues_total == 0) and (due.due_amount == 0):
                        print('none')

                    else:
                        context["dues"].append(
                            [member.member_number.normalize(), member.name_eng, due.due_display_id, due.due_type,
                             due.due_amount, dues_total, member.is_active])

            # Fetching Member Details
            if member.family_number in context["members"].keys():
                context["members"][member.family_number].append(
                    [member.name_eng, member.member_number.normalize(), member.is_active])
            else:
                context["members"][member.family_number] = [[]]
                context["members"][member.family_number][0] = (
                    member.name_eng, member.member_number.normalize(), member.is_active)

            # Fetching Receipt Records
        receipt_records = ReceiptsInvoice.objects.filter(family_no=member.family_number,
                                                         receipt_financial_year=get_financial_year(),
                                                         is_active=True).order_by('-receipt_date')
        # filter_receiptinvoices_by_family(member.family_number)

        for record in receipt_records:
            names = ""
            members = []
            receipts = record.receipt_ids.split('/')
            receipts.pop(-1)
            for receipt in receipts:
                receipt_no = Receipts.objects.get(receipt_id=receipt)
                if receipt_no.receipt_member not in members:
                    member = Members.objects.get(member_number=receipt_no.receipt_member)
                    names += member.name_eng + ','
                    members.append(receipt_no.receipt_member)
            names = names[:-1]
            context["familyreceipts"].append(
                [record.receipt_invoice_id, record.receipt_date, record.total_amount, names])
        return render(request, 'family_dues.html', context)

    if request.method == "POST":
        receipt_ids = ""
        total_amount = 0
        due_id_all = request.POST.getlist("due-id")
        for i in range(len(due_id_all)):
            due_id = request.POST.getlist("due-id")[i]
            member = request.POST.getlist("member-id")[i]
            amountraw = request.POST.getlist("amount")[i]
            if amountraw == '':
                continue
            else:
                amount = decimal.Decimal(amountraw)
            family = request.POST.getlist("family-id")[i]
            account_serial = Dues.objects.get(due_display_id=due_id,
                                              due_financial_year=get_financial_year()).account_serial
            if request.POST['btn'] == "submit-payment":
                txn_remarks = 'Normal Due Payment'
                receipt_ids += wf.due_payment_receipt_record_create(due_id, amount, member, family, account_serial,
                                                                    request.user.get_username(), txn_remarks) + '/'
                total_amount += amount

            else:
                txn_type = 'OVERRIDE'
                txn_remarks = 'Override'
                wf.ledger_record_create(due_id, txn_type, -int(amount), member, family, txn_remarks,
                                        account_serial, request.user.get_username())
        if request.POST['btn'] == "submit-payment":
            wf.receipt_invoice_record_create(receipt_ids, total_amount, family, request.user.get_username())

        return redirect('/dues/?family-dues=' + family)


@login_required()
def newdue(request):
    if request.method == 'POST':
        form = NewDue(request.POST)
        if form.is_valid():
            due_id = form.cleaned_data['due_id']
            due_type = form.cleaned_data['due_type']
            due_amount = form.cleaned_data['due_amount']
            due_fineamt = form.cleaned_data['due_fineamt']
            is_head = form.cleaned_data['is_head']
            is_retired = form.cleaned_data['is_retired']
            is_nonresident = form.cleaned_data['is_nonresident']
            is_govt = form.cleaned_data['is_govt']
            is_male = form.cleaned_data['is_male']
            account_serial = form.cleaned_data['account_serial']
            duecreation = Dues.objects.create(due_display_id=due_id, due_type=due_type, due_amount=due_amount,
                                              due_fineamt=due_fineamt, due_financial_year=get_financial_year(),
                                              is_head=is_head, is_retired=is_retired, is_nonresident=is_nonresident,
                                              is_govt=is_govt,
                                              is_male=is_male, due_active=1, account_serial=account_serial, applied=0,
                                              paid_together=0)
            return HttpResponse('<h1>Done</h1>')
    form = NewDue()
    return render(request, 'new-due.html', {'formdue': form})


@login_required()
def applydues(request):
    due_disp_id = request.POST['due_display_id']
    due = Dues.objects.get(due_financial_year=get_financial_year(), due_display_id=due_disp_id)
    members_list = Members.objects.filter(is_active=True)
    for member in members_list:
        if (((member.is_head == due.is_head) or (due.is_head == -1))
                and (member.is_due_apply is True)
                and ((member.is_retired == due.is_retired) or (due.is_retired == -1))
                and ((member.is_govt == due.is_govt) or (due.is_govt == -1))
                and ((member.is_male == due.is_male) or (due.is_male == -1) or member.is_head == 1)
                and ((member.is_nonresident == due.is_nonresident) or (due.is_nonresident == -1))
                and (member.is_alive is True)
                and (member.age >= 18)
                and ((member.member_number % 1 == 0) or member.is_head == 1)):
            txn_due_id = due.due_display_id
            txn_type = 'DUE'
            txn_amount = due.due_amount
            txn_member = member.member_number
            txn_family = member.family_number
            txn_remarks = 'Regular Due'
            wf.ledger_record_create(txn_due_id, txn_type, txn_amount, txn_member, txn_family, txn_remarks,
                                    due.account_serial, request.user.get_username())
    due.applied = 1
    due.save()
    return redirect('/dues-settings')


def get_member_dues_balance(member):
    balance_records = Ledger.objects.filter(txn_member__exact=member, txn_financial_year=get_financial_year())
    balance = 0
    for record in balance_records:
        balance += record.txn_amount
    return balance


# ACCOUNTS RELATED FUNCTIONS


@login_required()
def accountview(request):
    context = {}
    if request.method == "GET":
        context["accounts"] = []
        context["accountnames"] = []
        accs = Accounts.objects.order_by('account_serial')
        accrecords = AccountRecords.objects.all()
        for acc in accs:
            cash_in_hand = 0
            cash_in_bank = 0
            current_balance = 0
            for rec in accrecords:
                if int(rec.account_serial) == int(acc.account_serial):
                    cash_in_hand += rec.add_to_cash_in_hand
                    cash_in_bank += rec.add_to_cash_in_bank
                    current_balance += rec.add_to_current_balance
                    print(cash_in_hand,cash_in_bank,current_balance)
            context["accounts"].append(
                [acc.account_serial, acc.account_name, acc.opening_balance, cash_in_hand, cash_in_bank, current_balance,
                 accountsinfo(acc.account_serial), acc.bank_name])
            context["accountnames"].append([acc.account_serial, acc.account_name, acc.bank_name])

        context["txns"] = []
        txns = AccountTransactionRecords.objects.order_by('-txn_time')
        for txn in txns:
            context['txns'].append(
                ["TXN-" + str(get_financial_year()) + " #" + str(txn.txn_id), txn.account_serial, txn.account_name,
                 txn.account_number, txn.type, txn.amount, txn.login_user, txn.txn_time])

    if request.method == "POST":
        if request.POST['btn'] == 'deposit-withdraw':
            amount = decimal.Decimal(request.POST["amount"])
            type = request.POST["type"]
            account_serial = request.POST["account"]
            account = Accounts.objects.get(financial_year=get_financial_year(), account_serial=account_serial)
            AccountTransactionRecords.objects.create(account_serial=account_serial,
                                                     financial_year=get_financial_year(),
                                                     account_name=account.account_name,
                                                     account_number=account.account_number,
                                                     bank_name=account.bank_name, type=type, amount=amount,
                                                     login_user=request.user.get_username(),
                                                     txn_time=timezone.now())
            txn_id = AccountTransactionRecords.objects.all().last()

            if type == "Deposit":
                account.cash_in_hand -= amount
                account.cash_in_bank += amount
                AccountRecords.objects.create(account_serial=account_serial,
                                              financial_year=get_financial_year(),
                                              type="DEPOSIT", add_to_cash_in_hand=-amount,
                                              add_to_cash_in_bank=amount,
                                              add_to_current_balance=0, txn_time=timezone.now(),
                                              txn_ref_id=txn_id.txn_id,
                                              login_user=request.user.get_username())
            else:
                account.cash_in_hand += amount
                account.cash_in_bank -= amount
                AccountRecords.objects.create(account_serial=account_serial,
                                              financial_year=get_financial_year(),
                                              type="WITHDRAW", add_to_cash_in_hand=amount,
                                              add_to_cash_in_bank=-amount,
                                              add_to_current_balance=0, txn_time=timezone.now(),
                                              txn_ref_id=txn_id,
                                              login_user=request.user.get_username())
            account.save()
        elif request.POST['btn'] == 'transfer':
            amount = decimal.Decimal(request.POST["amount"])
            to_account_serial = request.POST["to-account"]
            from_account_serial = request.POST["from-account"]
            from_account = Accounts.objects.get(financial_year=get_financial_year(), account_serial=from_account_serial)
            to_account = Accounts.objects.get(financial_year=get_financial_year(), account_serial=to_account_serial)
            AccountTransactionRecords.objects.create(account_serial=from_account_serial,
                                                     financial_year=get_financial_year(),
                                                     account_name=from_account.account_name,
                                                     account_number=from_account.account_number,
                                                     bank_name=from_account.bank_name, type="Transfer (Out)",
                                                     amount=-amount,
                                                     login_user=request.user.get_username(),
                                                     txn_time=timezone.now())
            txn_id = AccountTransactionRecords.objects.all().last()
            AccountRecords.objects.create(account_serial=from_account_serial,
                                          financial_year=get_financial_year(),
                                          type="TRANSFER (OUT)", add_to_cash_in_hand=-amount,
                                          add_to_cash_in_bank=0,
                                          add_to_current_balance=-amount, txn_time=timezone.now(),
                                          txn_ref_id=txn_id.txn_id,
                                          login_user=request.user.get_username())
            AccountTransactionRecords.objects.create(account_serial=to_account_serial,
                                                     financial_year=get_financial_year(),
                                                     account_name=to_account.account_name,
                                                     account_number=to_account.account_number,
                                                     bank_name=to_account.bank_name, type="Transfer (In)",
                                                     amount=amount,
                                                     login_user=request.user.get_username(),
                                                     txn_time=timezone.now())
            txn_id = AccountTransactionRecords.objects.all().last()
            AccountRecords.objects.create(account_serial=to_account_serial,
                                          financial_year=get_financial_year(),
                                          type="TRANSFER (IN)", add_to_cash_in_hand=amount,
                                          add_to_cash_in_bank=0,
                                          add_to_current_balance=amount, txn_time=timezone.now(),
                                          txn_ref_id=txn_id.txn_id,
                                          login_user=request.user.get_username())
        elif request.POST['btn'] == 'new-account':
            type = request.POST["type"]
            name = request.POST["name"]
            acnum = request.POST["acnum"]
            balance = request.POST["balance"]
            Accounts.objects.create(financial_year=get_financial_year(), account_name=type, account_number=acnum,
                                    bank_name=name,
                                    is_active=1, opening_balance=balance, closing_balance=balance,
                                    current_balance=balance, cash_in_hand=0,
                                    cash_in_bank=balance, description='')
            latest = Accounts.objects.all().last()
            AccountRecords.objects.create(account_serial=latest.account_serial, financial_year=get_financial_year(),
                                          type="OPENING",
                                          add_to_cash_in_bank=balance, add_to_cash_in_hand=0,
                                          add_to_current_balance=balance,
                                          txn_time=timezone.now(),
                                          txn_ref_id="NA",
                                          login_user=request.user.get_username())

        return redirect('/account-reports')

    return render(request, 'account_view.html', context)


def accountsinfo(account_serial):
    account = Accounts.objects.get(financial_year=get_financial_year(), account_serial=account_serial)
    receipts = Receipts.objects.filter(receipt_financial_year=get_financial_year(),
                                       account_serial=account.account_serial, is_active=True)
    vouchers = Vouchers.objects.filter(voucher_financial_year=get_financial_year(),
                                       account_serial=account.account_serial)
    voucher_income = 0
    voucher_expense = 0
    receipt_income = 0
    for receipt in receipts:
        receipt_income += receipt.receipt_amount
    for voucher in vouchers:
        if voucher.voucher_type == "EXPENSE":
            voucher_expense += voucher.voucher_amount
        else:
            voucher_income += voucher.voucher_amount
    list = [format(voucher_income, '.2f'), format(voucher_expense, '.2f'), format(receipt_income, '.2f')]
    return list


@login_required()
def printinvoice(request):
    if request.method == "GET":
        try:
            data = {}
            invoice = request.GET["Receipt No."]
            receipt_records = ReceiptsInvoice.objects.get(receipt_invoice_id=invoice)
            receipts = receipt_records.receipt_ids.split('/')[:-1]
            print(receipts)
            recs = []
            total = 0
            for receipt in receipts:
                rec = Receipts.objects.get(receipt_id=receipt)
                member = rec.receipt_member
                due_disp_id = rec.receipt_due_id
                due_rec = Dues.objects.get(due_display_id=due_disp_id)
                member_rec = Members.objects.get(member_number=member, is_active=True)
                recs.append([due_rec.due_type, member_rec.name_eng, rec.receipt_amount])
                total += rec.receipt_amount
                data["invoice"] = {
                    "name": member_rec.name_eng,
                    "member_no": member.normalize(),
                    "receipt_no": invoice,
                    "date": rec.receipt_date,
                    "family_name": member_rec.family_name,
                    "area": member_rec.area,
                    "postbox": member_rec.postbox,
                    "recs": recs,
                    "total": total
                }
            return render(request, 'invoice.html', data)
        except:
            return HttpResponse("NO SUCH RECEIPT!")


@login_required()
def newmember(request):
    if request.method == 'POST':
        form = NewMember(request.POST)
        if form.is_valid():
            member_no = form.cleaned_data['member_no']
            family = form.cleaned_data['family_no']
            name = form.cleaned_data['name']
            is_due_apply = form.cleaned_data['is_due_apply']
            is_retired = form.cleaned_data['is_retired']
            is_nonresident = form.cleaned_data['is_nonresident']
            is_govt = form.cleaned_data['is_govt']
            is_male = form.cleaned_data['is_male']
            is_alive = form.cleaned_data['is_alive']
            age = form.cleaned_data['age']
            mobile = form.cleaned_data['mobile']
            email = form.cleaned_data['email']
            description = form.cleaned_data['description']
            remarks = form.cleaned_data['remarks']
            members = Members.objects.all()
            for member in members:
                if member.member_number == member_no:
                    return HttpResponse('Member with Member No.' + str(member_no) + ' already exists!')
            try:
                family_info = Members.objects.filter(family_number=family)[0]
                print(family_info)
            except Exception:
                return HttpResponse('<h1>Failed! No Such Family</h1>')
            membercreation = Members.objects.create(financial_year_serial=get_financial_year(),
                                                    member_number=member_no, family_number=family,
                                                    family_name=family_info.family_name, name_eng=name, is_active=1,
                                                    is_head=0,
                                                    is_due_apply=is_due_apply, is_retired=is_retired,
                                                    is_nonresident=is_nonresident,
                                                    is_govt=is_govt,
                                                    is_male=is_male, is_alive=is_alive, age=age, area=family_info.area,
                                                    postbox=family_info.postbox, address=family_info.address,
                                                    mobile=mobile, email=email, description=description,
                                                    remarks=remarks)
            return HttpResponse('<h1>Done</h1>')
    form = NewMember()
    return render(request, 'new-member.html', {'formdue': form})


@login_required()
def newfamily(request):
    exists = 0
    if request.method == 'POST':
        form = NewFamily(request.POST)
        if form.is_valid():
            member_no = form.cleaned_data['member_no']
            family_name = form.cleaned_data['family_name']
            area = form.cleaned_data['area']
            postbox = form.cleaned_data['postbox']
            address = form.cleaned_data['area']
            family = form.cleaned_data['family_no']
            name = form.cleaned_data['name']
            is_due_apply = form.cleaned_data['is_due_apply']
            is_retired = form.cleaned_data['is_retired']
            is_nonresident = form.cleaned_data['is_nonresident']
            is_govt = form.cleaned_data['is_govt']
            is_male = form.cleaned_data['is_male']
            is_alive = form.cleaned_data['is_alive']
            age = form.cleaned_data['age']
            mobile = form.cleaned_data['mobile']
            email = form.cleaned_data['email']
            description = form.cleaned_data['description']
            remarks = form.cleaned_data['remarks']
            last_member = Members.objects.all().count() + 1
            members = Members.objects.all()
            flag = True
            old_family = ''
            for member in members:
                if member.member_number == member_no:
                    to_delete = member
                    old_family = member.family_number
                    exists = 1
                if member.family_number == family:
                    flag = False

            if flag:
                if exists == 1:
                    to_delete.delete()
                membercreation = Members.objects.create(financial_year_serial=get_financial_year(),
                                                        member_number=member_no, family_number=family,
                                                        family_name=family_name, name_eng=name, is_active=1,
                                                        is_head=1,
                                                        is_due_apply=is_due_apply, is_retired=is_retired,
                                                        is_nonresident=is_nonresident,
                                                        is_govt=is_govt,
                                                        is_male=is_male, is_alive=is_alive, age=age, area=area,
                                                        postbox=postbox, address=address,
                                                        mobile=mobile, email=email, description=description,
                                                        remarks=remarks)
                x = ''
                if old_family != '':
                    x = 'Member successfully deactivated from family number ' + str(
                        old_family) + ' and added to ' + str(family)

                return HttpResponse('Done. Member Added Successfully.' + x)
            else:
                return HttpResponse('Family with family no. ' + str(family) + ' already exists!')
    form = NewFamily()
    return render(request, 'new-family.html', {'formdue': form})


@login_required()
def editmember(request):
    if request.method == 'POST':
        instance = Members.objects.get(member_number=request.POST['member_no'], is_active=1)
        family = instance.family_number
        form = EditMember(request.POST or None, instance=instance)
        if form.is_valid():
            if form.cleaned_data['family_number'] != family:
                if instance.is_head:
                    return HttpResponse(
                        instance.name_eng + " is the HEAD OF FAMILY! Family Number of the head cannot be updated!")
                else:
                    MemberFamilyChanges.objects.create(serial=instance.serial, old_family=family,
                                                       new_family=form.cleaned_data['family_number'])
            form.save()
            members = Members.objects.filter(family_number=family, is_active=True)
            for member in members:
                member.family_name = form.cleaned_data['family_name']
                member.area = form.cleaned_data['area']
                member.address = form.cleaned_data['address']
                member.postbox = form.cleaned_data['postbox']
                member.save()
            return HttpResponse('Member Updated')
        print(form.errors)
        return HttpResponse('Member Not Updated')
    else:
        member_no = request.GET['member_no']
        instance = Members.objects.get(member_number=member_no, is_active=1)
        form = EditMember(instance=instance, use_required_attribute=False)
        return render(request, 'edit-member.html', {'formdue': form, 'member_no': member_no})


@login_required()
def dueslist(request):
    dues = Dues.objects.all()
    dues = dues.extra(select={
        'serial_a': "SUBSTR(due_display_id, 3)",
        'serial_b': "CAST(substr(due_display_id, 4) AS DECIMAL)"})
    dues = dues.order_by('serial_b')
    list = []
    for due in dues:
        if due.due_display_id != 'DM-10':
            list.append(
                [due.due_display_id, due.due_type, due.due_amount, due.due_fineamt, due.applied, due.paid_together])
    return render(request, 'dues.html', {'dues': list})


@login_required()
def manual_due_apply(request):
    due_display_id = request.POST['due_display_id']
    member_no = decimal.Decimal(request.POST['member_no'])
    due = Dues.objects.get(due_financial_year=get_financial_year(), due_display_id=due_display_id)
    member = Members.objects.get(member_number=member_no, is_active=1)
    txn_id = int(timezone.now().strftime("%Y%m%d%H%M%S")) + random.randrange(20000000)
    txn_due_id = due.due_display_id
    txn_type = 'DUE'
    txn_amount = due.due_amount
    txn_member = member.member_number
    txn_family = member.family_number
    txn_remarks = 'Regular Due'
    wf.ledger_record_create(txn_due_id, txn_type, txn_amount, txn_member, txn_family, txn_remarks, due.account_serial,
                            request.user.get_username())

    return HttpResponse('<h1>Done</h1>')


@login_required()
def edit_dues(request):
    if request.method == 'POST':
        instance = Dues.objects.get(due_display_id=request.POST['duedisplayid'], due_active=1,
                                    due_financial_year=get_financial_year())
        form = EditDues(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponse('Due Updated')
        return HttpResponse('Due Not Updated. Internal Error.')
    else:
        duedisplayid = request.GET['duedisplayid']
        instance = Dues.objects.get(due_display_id=duedisplayid)
        form = EditDues(instance=instance, use_required_attribute=False)
        return render(request, 'edit-dues.html', {'formdue': form, 'duedisplayid': duedisplayid})


@login_required()
def override_due(request):
    due_disp_id = request.POST['due_display_id']
    due = Dues.objects.get(due_financial_year=get_financial_year(), due_display_id=due_disp_id)
    ledger = Ledger.objects.filter(txn_due_id=due_disp_id, txn_financial_year=get_financial_year())
    ledger.delete()
    due.applied = 0
    due.save()
    return redirect('/dues-settings/')


@login_required()
def mark_as_paid(request):
    due_disp_id = request.POST['due_display_id']
    due = Dues.objects.get(due_financial_year=get_financial_year(), due_display_id=due_disp_id)
    ledger = Ledger.objects.filter(txn_due_id=due_disp_id, txn_financial_year=get_financial_year())
    done = []
    for record in ledger:
        key = (record.txn_member, record.txn_due_id)

        if key not in done:
            memberduerecs = Ledger.objects.filter(txn_member=record.txn_member, txn_due_id=record.txn_due_id)
            due_id = due.due_display_id
            member = record.txn_member
            family = record.txn_family
            txn_remarks = 'MANUALLY MARKED AS PAID'
            account_serial = due.account_serial
            amount = 0
            for recs in memberduerecs:
                if recs.txn_type == "DUE":
                    amount += recs.txn_amount
                if recs.txn_type == "PAID":
                    amount += recs.txn_amount
            receipt = wf.due_payment_receipt_record_create(due_id, amount, member, family, account_serial,
                                                           request.user.get_username(), txn_remarks) + '/'
            wf.receipt_invoice_record_create(receipt, amount, family, request.user.get_username(),
                                             txn_remarks + '(' + due_id + ')')
            due.paid_together = True
            due.save()
            done.append(key)

    return redirect('/dues-settings/')


def cancel_receipt(request):
    invoice = request.POST["Receipt No."]
    family = request.POST["Family No."]
    receipt_records = ReceiptsInvoice.objects.get(receipt_invoice_id=invoice)
    receipts = receipt_records.receipt_ids.split('/')[:-1]
    for receipt in receipts:
        receipt_record = Receipts.objects.get(receipt_id=receipt)
        wf.ledger_record_create(receipt_record.receipt_due_id, "PAYMENT CANCELLED", receipt_record.receipt_amount,
                                receipt_record.receipt_member,
                                receipt_record.receipt_family, "Payment Cancelled", receipt_record.account_serial,
                                request.user.get_username())
        AccountRecords.objects.create(account_serial=receipt_record.account_serial, financial_year=get_financial_year(),
                                      type="CANCELLED RECEIPT",
                                      add_to_cash_in_hand=-(receipt_record.receipt_amount), add_to_cash_in_bank=0,
                                      add_to_current_balance=-(receipt_record.receipt_amount),
                                      txn_time=timezone.now(), txn_ref_id=receipt_record.txn_id,
                                      login_user=request.user.get_username())
        receipt_record.is_active = False
        receipt_record.save()
    receipt_records.is_active = False
    receipt_records.save()
    return redirect('/dues/?family-dues=' + family)


def undo_mark_as_paid(request):
    due_id = request.POST["due_display_id"]
    due = Dues.objects.get(due_display_id=due_id, due_financial_year=get_financial_year())
    remarks = 'MANUALLY MARKED AS PAID' + '(' + due_id + ')'
    receipt_records = ReceiptsInvoice.objects.filter(receipt_financial_year=get_financial_year(), remarks=remarks)
    for records in receipt_records:
        receipts = records.receipt_ids.split('/')[:-1]
        for receipt in receipts:
            receipt_record = Receipts.objects.get(receipt_id=receipt)
            ledger_record = Ledger.objects.get(txn_id=receipt_record.txn_id)
            AccountRecords.objects.create(account_serial=receipt_record.account_serial,
                                          financial_year=get_financial_year(),
                                          type="CANCELLED RECEIPT",
                                          add_to_cash_in_hand=-(receipt_record.receipt_amount), add_to_cash_in_bank=0,
                                          add_to_current_balance=-(receipt_record.receipt_amount),
                                          txn_time=timezone.now(), txn_ref_id=receipt_record.txn_id,
                                          login_user=request.user.get_username())
            ledger_record.delete()
            receipt_record.delete()
        records.delete()
    due.paid_together = False
    due.save()
    return redirect('/dues-settings/')
