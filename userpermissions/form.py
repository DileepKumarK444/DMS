from django import forms
from django.contrib.postgres.fields import ArrayField


class SaveRoleForm(forms.Form):
    role = forms.CharField(max_length=120)
    group = forms.CharField(required=False)
    description = forms.CharField(max_length=200, required=False)

    def clean(self):
        cleaned_data = super().clean()
        data_group = cleaned_data.get(
            "group") and cleaned_data.get("group") or []
        if len(data_group) == 0:
            self.add_error('group', 'This field is required.')


class SaveGroupForm(forms.Form):
    group = forms.CharField(max_length=120)
    description = forms.CharField(max_length=200, required=False)


class SavePermissionForm(forms.Form):
    permission = forms.CharField(max_length=120)
    description = forms.CharField(max_length=200, required=False)


class SaveGroupPermissionForm(forms.Form):
    group_id = forms.IntegerField()
    permission_id = forms.IntegerField()
