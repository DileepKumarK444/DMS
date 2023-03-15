from django import forms
# from django.core.validators import validate_integer

class SaveDroneFrom(forms.Form):
    sb_battery = forms.CharField(max_length=100)
    txt_modal = forms.CharField(max_length=100)
    txt_modal_no = forms.CharField(max_length=100)
    txt_serial_no = forms.CharField(max_length=100)
    txt_uin = forms.CharField(max_length=100)
    sb_drone_type = forms.CharField(max_length=100)
    sb_drone_purpose = forms.CharField(max_length=100)
    sb_rc = forms.CharField(max_length=100)
    sb_sensor = forms.CharField(max_length=100)
    sb_camera = forms.CharField(max_length=100)

    sb_fc = forms.CharField(max_length=100)
    sb_frame = forms.CharField(max_length=100)
    sb_qgc = forms.CharField(max_length=100)
    file = forms.FileField()
    mdi_file = forms.FileField()

class SaveDroneUpdateFrom(forms.Form):
    sb_battery = forms.CharField(max_length=100)
    txt_modal = forms.CharField(max_length=100)
    txt_modal_no = forms.CharField(max_length=100)
    txt_serial_no = forms.CharField(max_length=100)
    txt_uin = forms.CharField(max_length=100)
    sb_drone_type = forms.CharField(max_length=100)
    sb_drone_purpose = forms.CharField(max_length=100)
    sb_rc = forms.CharField(max_length=100)
    sb_sensor = forms.CharField(max_length=100)
    sb_camera = forms.CharField(max_length=100)

    sb_fc = forms.CharField(max_length=100)
    sb_frame = forms.CharField(max_length=100)
    sb_qgc = forms.CharField(max_length=100)
    # file = forms.FileField()
    # mdi_file = forms.FileField()
#     last_name = forms.CharField(max_length=100)
#     email = forms.EmailField()
#     phone = forms.IntegerField()
#     company = forms.CharField(max_length=100)
#     designation = forms.CharField(max_length=100)
#     country = forms.CharField(max_length=100)
#     state = forms.CharField(max_length=100)

    # def clean(self):
    #     cleaned_data = super().clean()
    #     phone = validate_integer(cleaned_data.get('phone', None))
    #     print(phone)
    #     if phone:
    #         self.add_error('phone', 'Enter valid phone number.')

class SaveConfigFrom(forms.Form):
    sb_template = forms.CharField(max_length=100)
    txt_mac_id = forms.CharField(max_length=100)
    txt_fc_id = forms.CharField(max_length=100)
    txt_host = forms.CharField(max_length=100)
    txt_port = forms.CharField(max_length=100)
    txt_username = forms.CharField(max_length=100)
    txt_password = forms.CharField(max_length=100)
    txt_folder_path = forms.CharField(max_length=100)
