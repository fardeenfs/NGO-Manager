from django.shortcuts import render
import decimal
from datetime import datetime
from django.shortcuts import render, redirect
from vouchers.models import Vouchers, VoucherTypes
from MainScreen.models import Members, Dues, Receipts, Ledger, Sitewide, Accounts, AccountTransactionRecords

from django.contrib.auth.decorators import login_required
import random
import csv
import pandas as pd

import io
import xlsxwriter
from django.http import HttpResponse, FileResponse

from django.http import HttpResponse

context = {}


def get_financial_year():
    financial_year = Sitewide.objects.latest('financial_id')
    return financial_year.financial_term_code


def getfamilies(rward):
    if rward != 'All':
        heads = Members.objects.filter(is_head=1, area=rward, is_active=1)
    else:
        heads = Members.objects.filter(is_head=1,is_active=1)
    heads = heads.order_by('serial')
    print(heads[0].serial_b)

    return heads


def getmembers(rward):
    if rward != 'All':
        members = Members.objects.filter(area=rward, is_active=1)
    else:
        members = Members.objects.filter(is_active=1)
    members = members.order_by('serial')
    return members


def getmembers_no_d(rward):
    memberslist = []
    if rward != 'All':
        members = Members.objects.filter(area=rward, is_active=1)
    else:
        members = Members.objects.filter(is_active=1)
    members = members.order_by('family_number')
    for member in members:
        if (member.is_head == 1) or float(member.member_number).is_integer():
            print(member)
            memberslist.append(member)
    return memberslist


@login_required()
def reportshome(request):
    if request.method == "GET":
        return render(request, 'reports.html')
    elif request.method == "POST":
        final = []
        rtype = request.POST["report-type"]
        rfilter = request.POST["filter-type"]
        rward = request.POST["ward-type"]
        if rtype == 'FamilyList':
            memlist = getfamilies(rward)
        elif rtype == 'MembersList':
            memlist = getmembers(rward)
        elif rtype == 'MembersListNoD':
            memlist = getmembers_no_d(rward)
        if rfilter == 'All':
            for member in memlist:
                final.append(member)
        if rfilter == 'NonResident':
            for member in memlist:
                if member.is_nonresident is True:
                    final.append(member)

        if rfilter == 'Employee':
            for member in memlist:
                if member.is_govt is True:
                    final.append(member)
        if rfilter == 'Retired':
            for member in memlist:
                if member.is_retired is True:
                    final.append(member)

        final_list = []
        for member in final:
            final_list.append(
                [member.serial, member.member_number, member.family_number,  member.name_eng,
                 member.family_name,
                 member.area, member.is_nonresident, member.is_govt, member.is_retired])
        buffer = io.BytesIO()
        workbook = xlsxwriter.Workbook(buffer)
        worksheet = workbook.add_worksheet()
        header = ['SERIAL', 'MEMBER NUMBER', 'FAMILY NUMBER', 'NAME', 'FAMILY NAME', 'AREA', 'NON RESIDENT?', 'GOVT?',
                  'RETIRED?']
        worksheet.write_row(0, 0, header)
        row = 1
        col = 0
        for member in final_list:
            worksheet.write_row(row, col, member)
            row += 1
        workbook.close()
        buffer.seek(0)

        return FileResponse(buffer, as_attachment=True, filename=rtype + '.xlsx')


@login_required()
def getkudishika(request):
    kudishika = Dues.objects.get(due_type='Kudishika', due_financial_year=get_financial_year())
    print(kudishika)
    final = {}
    kudishika_list = Ledger.objects.filter(txn_due_id=kudishika.due_display_id)
    for rec in kudishika_list:
        if rec.txn_member in final.keys():
            final[rec.txn_member] += rec.txn_amount
        else:
            final[rec.txn_member] = rec.txn_amount
    total = 0
    to_excel = []
    for key, value in final.items():
        try:
            member = Members.objects.get(member_number=key, is_active=1)
        except Exception:
            member = Members.objects.get(member_number=key)
        to_excel.append([member.serial, member.member_number, member.family_number, member.name_eng,
                         member.family_name, member.area, value])
        total += float(value)
    buffer = io.BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()
    header = ['SERIAL', 'MEMBER NUMBER', 'FAMILY NUMBER', 'NAME', 'AREA', 'FAMILY NAME', 'AMOUNT']
    worksheet.write_row(0, 0, header)
    row = 1
    col = 0
    for member in to_excel:
        worksheet.write_row(row, col, member)
        row += 1
    worksheet.write(row + 1, 6, "TOTAL")
    worksheet.write(row + 1, 7, total)
    workbook.close()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename="Kudishika" + '.xlsx')


@login_required()
def incomevoucher(request):
    if request.POST['btn'] == 'monthly':
        start = request.POST['startdate']
        end = request.POST['enddate']
        vouchers = Vouchers.objects.filter(voucher_type='INCOME', voucher_date__range=[start, end]).order_by(
            'voucher_date')
        to_excel = []
        for voucher in vouchers:
            to_excel.append([str(voucher.voucher_display_id), voucher.voucher_date.strftime("%Y-%m-%d"), voucher.voucher_type,
                             voucher.voucher_head, voucher.voucher_subhead, voucher.voucher_amount,
                             voucher.voucher_member_name,
                             voucher.voucher_member_address, voucher.remarks])
        buffer = io.BytesIO()
        workbook = xlsxwriter.Workbook(buffer)
        worksheet = workbook.add_worksheet()
        header = ['RECORD ID', 'RECORD DATE', 'RECORD TYPE', 'RECORD HEAD', 'RECORD SUBHEAD', 'AMOUNT', 'NAME',
                  'ADDRESS', 'REMARKS']
        worksheet.write_row(0, 0, header)
        row = 1
        col = 0
        for member in to_excel:
            worksheet.write_row(row, col, member)
            row += 1
        workbook.close()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True,
                            filename="Income Records Report Custom(" + str(start) + ' to ' + end + ').xlsx')
    else:
        voucher_types = VoucherTypes.objects.all()
        voucher_types = voucher_types.order_by('voucher_head')
        to_excel = []
        for voucher_type in voucher_types:
            vouchers = Vouchers.objects.filter(voucher_type='INCOME', voucher_financial_year=get_financial_year(),
                                               voucher_reference_id=voucher_type.serial)
            total = 0
            for voucher in vouchers:
                total += voucher.voucher_amount
            if total != 0:
                to_excel.append(
                    [voucher_type.voucher_head, voucher_type.type,
                     total])
        buffer = io.BytesIO()
        workbook = xlsxwriter.Workbook(buffer)
        worksheet = workbook.add_worksheet()
        header = ['RECORD HEAD', 'RECORD TYPE', 'AMOUNT']
        worksheet.write_row(0, 0, header)
        row = 1
        col = 0
        for member in to_excel:
            worksheet.write_row(row, col, member)
            row += 1
        workbook.close()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True,
                            filename="Income Records Report Annual" + ".xlsx")


@login_required()
def expensevoucher(request):
    if request.POST['btn'] == 'monthly':
        start = request.POST['startdate']
        end = request.POST['enddate']
        vouchers = Vouchers.objects.filter(voucher_type='EXPENSE', voucher_date__range=[start, end]).order_by(
            'voucher_date')
        to_excel = []
        for voucher in vouchers:
            to_excel.append([str(voucher.voucher_display_id), voucher.voucher_date.strftime("%Y-%m-%d"), voucher.voucher_type,
                             voucher.voucher_head,
                             voucher.voucher_amount, voucher.voucher_member_name,
                             voucher.voucher_member_address, voucher.remarks])
        buffer = io.BytesIO()
        workbook = xlsxwriter.Workbook(buffer)
        worksheet = workbook.add_worksheet()
        header = ['RECORD ID', 'RECORD DATE', 'RECORD TYPE', 'RECORD HEAD','AMOUNT', 'NAME',
                  'ADDRESS', 'REMARKS']
        worksheet.write_row(0, 0, header)
        row = 1
        col = 0
        for member in to_excel:
            worksheet.write_row(row, col, member)
            row += 1
        workbook.close()
        buffer.seek(0)

        return FileResponse(buffer, as_attachment=True,
                            filename="Expense Records Report Custom(" + str(start) + ' to ' + end + ').xlsx')
    else:
        voucher_types = VoucherTypes.objects.all()
        voucher_types = voucher_types.order_by('voucher_head')
        to_excel = []
        for voucher_type in voucher_types:
            vouchers = Vouchers.objects.filter(voucher_type='EXPENSE', voucher_financial_year=get_financial_year(),
                                               voucher_reference_id=voucher_type.serial)
            total = 0
            for voucher in vouchers:
                total += voucher.voucher_amount
            if total != 0:
                to_excel.append(
                    [voucher_type.voucher_head,voucher_type.type,
                     total])
        buffer = io.BytesIO()
        workbook = xlsxwriter.Workbook(buffer)
        worksheet = workbook.add_worksheet()
        header = ['RECORD HEAD','RECORD TYPE', 'AMOUNT']
        worksheet.write_row(0, 0, header)
        row = 1
        col = 0
        for member in to_excel:
            worksheet.write_row(row, col, member)
            row += 1
        workbook.close()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True,
                            filename="Expense Records Report Annual" + ".xlsx")


@login_required()
def due_paid_reports(request):
    if request.POST['btn'] == 'yearly':
        receipts = Receipts.objects.filter(is_active=True).order_by('receipt_family')
    else:
        receipts = Receipts.objects.filter(is_active=True, receipt_date__gte=request.POST['startdate'],
                                           receipt_date__lte=request.POST['enddate']).order_by('receipt_family')
    context = {}
    for record in receipts:
        if record.receipt_due_id in context.keys():
            if record.receipt_member in context[record.receipt_due_id].keys():
                context[record.receipt_due_id][record.receipt_member] += abs(record.receipt_amount)
            else:
                context[record.receipt_due_id][record.receipt_member] = abs(record.receipt_amount)
        else:
            context[record.receipt_due_id] = {}
            context[record.receipt_due_id][record.receipt_member] = abs(record.receipt_amount)
    buffer = io.BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    for due_id in context.keys():
        due = Dues.objects.get(due_display_id=due_id)
        worksheet = workbook.add_worksheet(due.due_type)
        header = ['MEMBER NUMBER', 'MEMBER NAME', 'FAMILY NUMBER', 'FAMILY NAME', 'TYPE', 'AMOUNT']
        worksheet.write_row(0, 0, header)
        row = 1
        col = 0
        for member in context[due_id]:
            try:
                member_details = Members.objects.get(member_number=member)
            except:
                member_details = Members.objects.get(member_number=member, is_active=1)
            worksheet.write_row(row, col, [member, member_details.name_eng, member_details.family_number,
                                           member_details.family_name,
                                           due.due_type, context[due_id][member]])
            row += 1

    workbook.close()
    buffer.seek(0)
    if request.POST['btn'] == 'yearly':
        return FileResponse(buffer, as_attachment=True,
                            filename="Paid Dues Report Annual" + ".xlsx")
    else:
        return FileResponse(buffer, as_attachment=True,
                            filename="Paid Dues Report (" + request.POST['startdate'] + ' to ' + request.POST[
                                'enddate'] + ").xlsx")


@login_required()
def due_not_paid_reports(request):
    if request.POST['btn'] == 'yearly':
        ledger = Ledger.objects.all().order_by('txn_family')
    else:
        ledger = Ledger.objects.filter(txn_date__gte=request.POST['startdate'],
                                       txn_date__lte=request.POST['enddate']).order_by('txn_family')
    context = {}
    for record in ledger:
        if record.txn_due_id in context.keys():
            if record.txn_member in context[record.txn_due_id].keys():
                context[record.txn_due_id][record.txn_member] += record.txn_amount
            else:
                context[record.txn_due_id][record.txn_member] = record.txn_amount
        else:
            context[record.txn_due_id] = {}
            context[record.txn_due_id][record.txn_member] = record.txn_amount
    print(context)
    buffer = io.BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    for due_id in context.keys():
        due = Dues.objects.get(due_display_id=due_id)
        worksheet = workbook.add_worksheet(due.due_type)
        header = ['MEMBER NUMBER', 'MEMBER NAME', 'FAMILY NUMBER', 'FAMILY NAME', 'TYPE', 'AMOUNT']
        worksheet.write_row(0, 0, header)
        row = 1
        col = 0
        for member in context[due_id]:
            if context[due_id][member]>0:
                try:
                    member_details = Members.objects.get(member_number=member)
                except:
                    member_details = Members.objects.get(member_number=member, is_active=1)
                worksheet.write_row(row, col, [member, member_details.name_eng, member_details.family_number,
                                               member_details.family_name,
                                               due.due_type, context[due_id][member]])
                row += 1

    workbook.close()
    buffer.seek(0)
    if request.POST['btn'] == 'yearly':
        return FileResponse(buffer, as_attachment=True,
                            filename="Unpaid Dues Report Annual" + ".xlsx")
    else:
        return FileResponse(buffer, as_attachment=True,
                            filename="Unpaid Dues Report (" + request.POST['startdate'] + ' to ' + request.POST[
                                'enddate'] + ").xlsx")


@login_required()
def cancelled_due_reports(request):
    if request.POST['btn'] == 'yearly':
        ledger = Ledger.objects.filter(txn_type='OVERRIDE').order_by('txn_family')
    else:
        ledger = Ledger.objects.filter(txn_type='OVERRIDE', txn_date__gte=request.POST['startdate'],
                                       txn_date__lte=request.POST['enddate']).order_by('txn_family')
    context = {}
    for record in ledger:
        if record.txn_member in context.keys():
            if record.txn_due_id in context[record.txn_member].keys():
                context[record.txn_member][record.txn_due_id] += abs(record.txn_amount)
            else:
                context[record.txn_member][record.txn_due_id] = abs(record.txn_amount)
        else:
            context[record.txn_member] = {}
            context[record.txn_member][record.txn_due_id] = abs(record.txn_amount)
    print(context)
    to_excel = []
    for member in context.keys():
        try:
            member_details = Members.objects.get(member_number=member)
        except:
            member_details = Members.objects.get(member_number=member, is_active=1)
        if len(list(context[member].keys())) == 1:
            due_id = list(context[member].keys())[0]
            due = Dues.objects.get(due_display_id=due_id)
            to_excel.append(
                [member, member_details.name_eng, member_details.family_number, member_details.family_name,
                 due.due_type, context[member][due_id]])
        else:
            due_ids = list(context[member].keys())
            for due_id in due_ids:
                due = Dues.objects.get(due_display_id=due_id)
                to_excel.append(
                    [member, member_details.name_eng, member_details.family_number, member_details.family_name,
                     due.due_type, context[member][due_id]])
    buffer = io.BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()
    header = ['MEMBER NUMBER', 'MEMBER NAME', 'FAMILY NUMBER', 'FAMILY NAME', 'TYPE', 'AMOUNT']
    worksheet.write_row(0, 0, header)
    row = 1
    col = 0
    for member in to_excel:
        worksheet.write_row(row, col, member)
        row += 1
    workbook.close()
    buffer.seek(0)
    if request.POST['btn'] == 'yearly':
        return FileResponse(buffer, as_attachment=True,
                            filename="Cancelled Dues Report Annual" + ".xlsx")
    else:
        return FileResponse(buffer, as_attachment=True,
                            filename="Cancelled Dues Report (" + request.POST['startdate'] + ' to ' + request.POST[
                                'enddate'] + ").xlsx")


@login_required()
def inactive_members_reports(request):
    members = Members.objects.all()
    context = {}
    for member in members:
        if member.member_number in context.keys():
            if context[member.member_number] is False:
                context[member.member_number] = member.is_active
        else:
            context[member.member_number] = member.is_active
    to_excel = []
    for member in context.keys():
        if context[member] is False:
            member = Members.objects.get(member_number=member, is_active=False)
            to_excel.append([member.serial, member.member_number, member.name_eng, member.family_number, member.family_name,
                             member.remarks, member.area])
    buffer = io.BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()
    header = ['SERIAL', 'MEMBER NUMBER', 'MEMBER NAME', 'FAMILY NUMBER', 'FAMILY NAME', 'REASON', 'AREA']
    worksheet.write_row(0, 0, header)
    row = 1
    col = 0
    for member in to_excel:
        worksheet.write_row(row, col, member)
        row += 1
    workbook.close()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True,
                        filename="Inactive Members Report" + ".xlsx")

