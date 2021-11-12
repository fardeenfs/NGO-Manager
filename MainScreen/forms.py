from django import forms

from MainScreen.models import Members, Dues

choice = (
    (1, "Included"),
    (0, "Excluded"),
    (-1, "Not Applicable")
)


class NewDue(forms.Form):
    due_id = forms.CharField(label='Due ID')
    due_type = forms.CharField(label='Due Type')
    due_amount = forms.DecimalField(label='Due Amount')
    due_fineamt = forms.DecimalField(label='Fine Amount (Yearly)')
    is_head = forms.ChoiceField(choices=choice, label='Is Head?')
    is_retired = forms.ChoiceField(choices=choice, label='Is Retired?')
    is_nonresident = forms.ChoiceField(choices=choice,label='Is Non-Resident?')
    is_employee = forms.ChoiceField(choices=choice, label='Is Employee?')
    is_male = forms.ChoiceField(choices=choice, label='Is Male?')
    account_serial = forms.CharField(label='Account Serial')




class NewMember(forms.Form):
    family_no = forms.IntegerField()
    member_no = forms.DecimalField(max_digits=1000, decimal_places=2)
    name = forms.CharField()
    is_due_apply = forms.BooleanField(label='Is Due Apply?')
    is_retired = forms.BooleanField(required=False, label='Is Retired?')
    is_nonresident = forms.BooleanField(required=False, label='Is Non-Resident?')
    is_employee = forms.BooleanField(required=False, label='Is Employee?')
    is_male = forms.BooleanField(required=False, label='Is Male?')
    is_alive = forms.BooleanField(required=False, label='Is Alive?')
    age = forms.IntegerField()
    mobile = forms.IntegerField(required=False)
    email = forms.CharField(required=False)
    description = forms.CharField(required=False)
    remarks = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(NewMember, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['cols'] = 40


class NewFamily(forms.Form):
    family_no = forms.IntegerField()
    family_name = forms.CharField()
    area = forms.CharField()
    postbox = forms.CharField()
    address = forms.CharField()
    member_no = forms.DecimalField(max_digits=1000, decimal_places=2)
    name = forms.CharField()
    is_due_apply = forms.BooleanField(label='Is Due Apply?')
    is_retired = forms.BooleanField(required=False, label='Is Retired?')
    is_nonresident = forms.BooleanField(required=False, label='Is Non-Resident?')
    is_employee = forms.BooleanField(required=False, label='Is Employee?')
    is_male = forms.BooleanField(required=False, label='Is Male?')
    is_alive = forms.BooleanField(required=False, label='Is Alive?')
    age = forms.IntegerField()
    mobile = forms.IntegerField(required=False)
    email = forms.CharField(required=False)
    description = forms.CharField(required=False)
    remarks = forms.CharField(required=False)


class EditMember(forms.ModelForm):
    class Meta:
        model = Members
        exclude = ['serial', 'financial_year_serial', 'member_number',
                   'description']

    def __init__(self, *args, **kwargs):
        super(EditMember, self).__init__(*args, **kwargs)
        self.fields['name_eng'].widget.attrs['cols'] = 22
        self.fields['name_eng'].widget.attrs['rows'] = 1
        self.fields['family_name'].widget.attrs['cols'] = 22
        self.fields['family_name'].widget.attrs['rows'] = 1
        self.fields['family_number'].widget.attrs['cols'] = 22
        self.fields['family_number'].widget.attrs['rows'] = 1
        self.fields['email'].widget.attrs['cols'] = 22
        self.fields['email'].widget.attrs['rows'] = 1
        self.fields['area'].widget.attrs['cols'] = 22
        self.fields['area'].widget.attrs['rows'] = 1
        self.fields['address'].widget.attrs['cols'] = 22
        self.fields['address'].widget.attrs['rows'] = 1
        self.fields['remarks'].widget.attrs['cols'] = 22
        self.fields['remarks'].widget.attrs['rows'] = 1
        self.fields['postbox'].widget.attrs['cols'] = 22
        self.fields['postbox'].widget.attrs['rows'] = 1

        self.validate = kwargs.pop('validate', False)
        self.fields['email'].required = False
        self.fields['family_name'].required = False
        self.fields['mobile'].required = False
        self.fields['remarks'].required = False
        self.fields['address'].required = False
        self.fields['area'].required = False
        self.fields['postbox'].required = False

        self.fields['name_eng'].label = "Name"
        self.fields['is_active'].label = "Is Active?"
        self.fields['is_head'].label = "Is Head?"
        self.fields['is_due_apply'].label = "Is Due Apply?"
        self.fields['is_retired'].label = "Is Retired?"
        self.fields['is_nonresident'].label = "Is Non-Resident?"
        self.fields['is_employee'].label = "Is Employee"
        self.fields['is_male'].label = "Is Male?"
        self.fields['is_alive'].label = "Is Alive?"


class EditDues(forms.ModelForm):
    class Meta:
        model = Dues
        exclude = ['account_serial', 'due_display_id', 'due_financial_year', 'due_type', 'applied']

    def __init__(self, *args, **kwargs):
        super(EditDues, self).__init__(*args, **kwargs)
        self.fields['due_amount'].label = "Due Amount"
        self.fields['due_fineamt'].label = "Due Fine Amount"
        self.fields['is_head'].label = "Is Head?"
        self.fields['is_retired'].label = "Is Retired?"
        self.fields['is_nonresident'].label = "Is Non-Resident?"
        self.fields['is_govt'].label = "Is Govt"
        self.fields['is_male'].label = "Is Male?"
        self.fields['due_active'].label = "Due Active?"
