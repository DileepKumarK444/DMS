from django import forms

class FrmResetPassword(forms.Form):
    password = forms.CharField(min_length=8,max_length=15)
    confirm_password = forms.CharField(min_length=8,max_length=15)
