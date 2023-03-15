from django import forms


class SaveUserForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)
    role = forms.CharField()
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
    confirm_password = forms.CharField(max_length=100)


class EditUserForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    role = forms.CharField()
