# coding=utf-8
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.widgets import AdminDateWidget 
from registration.forms import RegistrationForm
from registration.signals import user_registered
from aidsbank.models import Applicant, Loan, Asset, Movement, AssetComment

"""
Authentication form
"""
class UserAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(UserAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control input-sm'
        self.fields['password'].widget.attrs['class'] = 'form-control input-sm'

"""
New user registration form
"""
class UserRegistrationForm(RegistrationForm):

    firstname = forms.CharField(label=u'Nome', max_length=64)
    lastname = forms.CharField(label=u'Cognome', max_length=64)
    address = forms.CharField(label=u'Indirizzo', max_length=128)
    city = forms.CharField(label=u'Città', max_length=128)
    cap = forms.CharField(label=u'CAP', max_length=5)
    province = forms.CharField(label=u'Provincia', max_length=128)
    phone = forms.CharField(label=u'Telefono', max_length=128)
    privacy = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'required'}),
            label=u'Informativa privacy',
            error_messages={'required': "Devi accettare i termini e le condizioni d'uso per registrarti"},
            help_text = u'Nullam convallis tellus quis massa hendrerit fringilla! Ut at mi id lectus feugiat ultricies pulvinar vel enim. Cras ut dolor et est cursus cursus. Fusce condimentum, ante non sollicitudin laoreet, est tortor consectetur nibh, quis ultricies enim arcu ut leo. Duis tincidunt purus et augue laoreet vel rutrum tellus sagittis. Suspendisse potenti. Integer vitae nisi tellus. ');

"""
Applicant profile form
"""
class ApplicantProfileForm(forms.ModelForm):

    class Meta:
        model = Applicant
        exclude = ('user',)

"""
asset request, only submit buttons
"""
class AssetRequestForm(forms.Form):
    pass

"""
Loan editing, manager
"""
class LoanEditManagerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(LoanEditManagerForm, self).__init__(*args, **kwargs)
        self.fields['loan_date'].widget.attrs['class'] = 'calendar'
    class Meta:
        model = Loan
        fields = ['asset', 'applicant', 'reservation_date', 'status', 'addressee', 'place', 'deposit', 'loan_date', 'loan_duration', 'renewal_date', 'return_date', 'solicit_date', 'follow_up', 'notes', 'renewal_available']
        widgets = {'asset': forms.HiddenInput(), 'applicant': forms.HiddenInput(), 'status': forms.HiddenInput(), 'reservation_date': forms.HiddenInput()}

"""
Asset creation, manager
"""
class AssetCreateManagerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AssetCreateManagerForm, self).__init__(*args, **kwargs)
        self.fields['invoice_date'].widget.attrs['class'] = 'calendar'
    class Meta:
        model = Asset

"""
Asset edit, manager
"""
class AssetForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AssetForm, self).__init__(*args, **kwargs)
        self.fields['invoice_date'].widget.attrs['class'] = 'calendar'
    class Meta:
        model = Asset

"""
Movement creation, manager
"""
class MovementCreateManagerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(MovementCreateManagerForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget.attrs['class'] = 'calendar'

    class Meta:
        model = Movement
        fields = ['date', 'type', 'status', 'notes']

"""
Asset comment creation, manager
"""
class AssetCommentCreateManagerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AssetCommentCreateManagerForm, self).__init__(*args, **kwargs)
    class Meta:
        model = AssetComment
        widgets = {'asset': forms.HiddenInput(), 'applicant': forms.HiddenInput(), 'published': forms.HiddenInput(), 'date': forms.HiddenInput()}

"""
Asset comment approval, manager
"""
class AssetCommentApproveManagerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AssetCommentApproveManagerForm, self).__init__(*args, **kwargs)
    class Meta:
        model = AssetComment
        widgets = {'asset': forms.HiddenInput(), 'applicant': forms.HiddenInput(), 'published': forms.HiddenInput(), 'date': forms.HiddenInput(), 'text': forms.HiddenInput()}
