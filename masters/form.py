"""
Master Form
"""
# pylint: disable=E0401
from django import forms
from django.core.validators import RegexValidator
from django.forms import ModelForm
from masters.models import ProductType, Category, Country, State, DmsSetting, DroneStatus, LogTemplate,Customer
from drone_management.models import DronePurpose,DroneType
from django.core.exceptions import ValidationError
class SaveCustomer(forms.Form): # pylint: disable=too-few-public-methods
    
    """Save Customer"""
    first_name = forms.CharField(max_length=100)
    email = forms.EmailField(required=False)
    phone = forms.CharField(max_length=13, validators=[RegexValidator(
        r'^(\+\d{1,3})?,?\s?\d{8,13}', message="Enter a valid phone number")])
    country = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    activation_date = forms.CharField(max_length=100)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        if not email:
            msg = forms.ValidationError("This field is required.")
            self.add_error('email', msg)

        type_check = Customer.objects.filter(email=email).count()
        if type_check:
            msg = forms.ValidationError("Sorry! email already exist.")
            self.add_error('email', msg)

class UpdateCustomer(forms.Form): # pylint: disable=too-few-public-methods
    
    """Save Customer"""

    def __init__(self,cid, *args, **kwargs):
        super(UpdateCustomer, self).__init__(*args, **kwargs)
        self.cid = cid

    first_name = forms.CharField(max_length=100)
    email = forms.EmailField(required=False)
    phone = forms.CharField(max_length=13, validators=[RegexValidator(
        r'^(\+\d{1,3})?,?\s?\d{8,13}', message="Enter a valid phone number")])
    country = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    activation_date = forms.CharField(max_length=100)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        if not email:
            msg = forms.ValidationError("This field is required.")
            self.add_error('email', msg)

        type_check = Customer.objects.filter(email=email).exclude(id=self.cid).count()
        if type_check:
            msg = forms.ValidationError("Sorry! email already exist.")
            self.add_error('email', msg)

class SaveCustomerUser(forms.Form): # pylint: disable=too-few-public-methods
    """Save Customer User"""
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=13, validators=[RegexValidator(
        r'^(\+\d{1,3})?,?\s?\d{8,13}', message="Enter a valid phone number")])
    password = forms.CharField(min_length=8,max_length=15)
    confirm_password = forms.CharField(min_length=8,max_length=15)

class SaveProduct(forms.Form): # pylint: disable=too-few-public-methods
    """Save Product"""
    dt_purchase = forms.CharField(max_length=100)
    cb_product_type = forms.CharField(max_length=100)
    cb_category = forms.CharField(max_length=100)
    txt_serial_no = forms.CharField(max_length=100)

class UpdateProduct(forms.Form): # pylint: disable=too-few-public-methods
    """Update Product"""
    dt_purchase = forms.CharField(max_length=100)
    cb_product_type = forms.CharField(max_length=100)
    cb_category = forms.CharField(max_length=100)
    txt_serial_no = forms.CharField(max_length=100)

class FrmResetPassword(forms.Form): # pylint: disable=too-few-public-methods
    """Reset Password"""
    password = forms.CharField(min_length=8,max_length=15)
    confirm_password = forms.CharField(min_length=8,max_length=15)

# class SaveProductType(forms.Form): # pylint: disable=too-few-public-methods
#     """Save Product Type"""
#     txt_name = forms.CharField(max_length=100)
#     cb_type = forms.CharField(max_length=100)

class SaveProductType(forms.Form): # pylint: disable=too-few-public-methods
    txt_name = forms.CharField(required=False)
    cb_type = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        txt_name = cleaned_data.get("txt_name")
        cb_type = cleaned_data.get("cb_type")

        if not txt_name:
            msg = forms.ValidationError("This field is required.")
            self.add_error('txt_name', msg)

        if not cb_type:
            msg = forms.ValidationError("This field is required.")
            self.add_error('cb_type', msg)

        type_check = ProductType.objects.filter(name=txt_name,type=cb_type).count()
        if type_check:
            msg = forms.ValidationError("Sorry! Product type already exist.")
            self.add_error('txt_name', msg)
            
class UpdateProductType(forms.Form): # pylint: disable=too-few-public-methods
    txt_name = forms.CharField(required=False)
    cb_type = forms.CharField(required=False)
    typeid = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        txt_name = cleaned_data.get("txt_name")
        cb_type = cleaned_data.get("cb_type")
        typeid = cleaned_data.get("typeid")

        if not txt_name:
            msg = forms.ValidationError("This field is required.")
            self.add_error('txt_name', msg)

        if not cb_type:
            msg = forms.ValidationError("This field is required.")
            self.add_error('cb_type', msg)

        type_check = ProductType.objects.filter(name=txt_name,type=cb_type).exclude(id=typeid).count()
        if type_check:
            msg = forms.ValidationError("Sorry! Product type already exist.")
            self.add_error('txt_name', msg)
        
    # def clean_txt_name(self):
    #     data = self.cleaned_data['txt_name']
    #     if data == '':
    #         raise ValidationError("You have forgotten about Fred!")
    #     return data
    # def clean_type(self):
    #     type = self.cleaned_data['cb_type']
    #     if not type:
    #         raise ValidationError("You have forgotten about type!")
    #     return type


    
    # txt_name = forms.CharField(max_length=100)
    # cb_type = forms.CharField(max_length=100)



# class SaveCategory(forms.Form): # pylint: disable=too-few-public-methods
#     """Save Category"""
#     dt_purchase = forms.CharField(max_length=100)

# class SaveCategory(forms.Form): # pylint: disable=too-few-public-methods
#     """Save Category"""
#     product_type = forms.CharField(max_length=100)
#     txt_model = forms.CharField(max_length=100)

class SaveCategory(forms.Form): # pylint: disable=too-few-public-methods
    """Save Category"""
    product_type = forms.IntegerField(required=False)
    txt_model = forms.CharField(required=False)
    print('123242234')
    def clean(self):
        cleaned_data = super().clean()
        product_type = cleaned_data.get("product_type")
        txt_model = cleaned_data.get("txt_model")

        if not product_type:
            msg = forms.ValidationError("This field is required.")
            self.add_error('product_type', msg)

        if not txt_model:
            msg = forms.ValidationError("This field is required.")
            self.add_error('txt_model', msg)

        type_check = Category.objects.filter(model=txt_model,type = product_type).count()
        if type_check:
            msg = forms.ValidationError("Sorry! Category already exist.")
            self.add_error('txt_model', msg)

class UpateCategory(forms.Form): # pylint: disable=too-few-public-methods
    """Save Category"""
    product_type = forms.IntegerField(required=False)
    txt_model = forms.CharField(required=False)
    catid = forms.IntegerField(required=False)
    
    def clean(self):
        cleaned_data = super().clean()
        product_type = cleaned_data.get("product_type")
        txt_model = cleaned_data.get("txt_model")
        catid = cleaned_data.get("catid")

        if not product_type:
            msg = forms.ValidationError("This field is required.")
            self.add_error('product_type', msg)

        if not txt_model:
            msg = forms.ValidationError("This field is required.")
            self.add_error('txt_model', msg)

        type_check = Category.objects.filter(model=txt_model,type = product_type).exclude(id=catid).count()
        if type_check:
            msg = forms.ValidationError("Sorry! Category already exist.")
            self.add_error('txt_model', msg)

class SaveTemplate(forms.Form): # pylint: disable=too-few-public-methods
    """Save Template"""
    txt_template_name = forms.CharField(required=False)
    log_fields = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        txt_template_name = cleaned_data.get("txt_template_name")
        log_fields = cleaned_data.get("log_fields")
        
        if not txt_template_name:
            msg = forms.ValidationError("This field is required.")
            self.add_error('txt_template_name', msg)
        if not log_fields:
            msg = forms.ValidationError("This field is required.")
            self.add_error('log_fields', msg)
        
        type_check = LogTemplate.objects.filter(template_name=txt_template_name).count()
        if type_check:
            msg = forms.ValidationError("Sorry! Template already exist.")
            self.add_error('txt_template_name', msg)

class UpdateTemplate(forms.Form): # pylint: disable=too-few-public-methods
    """Save Template"""
    txt_template_name = forms.CharField(required=False)
    log_fields = forms.CharField(required=False)
    id = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        txt_template_name = cleaned_data.get("txt_template_name")
        log_fields = cleaned_data.get("log_fields")
        id = cleaned_data.get("id")
        
        if not txt_template_name:
            msg = forms.ValidationError("This field is required.")
            self.add_error('txt_template_name', msg)
        if not log_fields:
            msg = forms.ValidationError("This field is required.")
            self.add_error('log_fields', msg)
        
        type_check = LogTemplate.objects.filter(template_name=txt_template_name).exclude(id=id).count()
        if type_check:
            msg = forms.ValidationError("Sorry! Template already exist.")
            self.add_error('txt_template_name', msg)

class GetFieldsForm(forms.Form): # pylint: disable=too-few-public-methods
    """Get Fields Form"""
    txt_template_name = forms.CharField(max_length=80)
    txt_file = forms.FileField()

class SaveSettingsForm(forms.Form): # pylint: disable=too-few-public-methods
    """Save Settings Form"""
    conf_key = forms.CharField(required=False)
    conf_value = forms.CharField(required=False)
    description = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        conf_key = cleaned_data.get("conf_key")
        conf_value = cleaned_data.get("conf_value")
        description = cleaned_data.get("description")
        
        if not conf_key:
            msg = forms.ValidationError("This field is required.")
            self.add_error('conf_key', msg)
        if not conf_value:
            msg = forms.ValidationError("This field is required.")
            self.add_error('conf_value', msg)
        if not description:
            msg = forms.ValidationError("This field is required.")
            self.add_error('description', msg)

        type_check = DmsSetting.objects.filter(conf_key=conf_key).count()
        if type_check:
            msg = forms.ValidationError("Sorry! Settings already exist.")
            self.add_error('conf_key', msg)
class UpdateSettingsForm(forms.Form): # pylint: disable=too-few-public-methods
    """Save Settings Form"""
    conf_key = forms.CharField(required=False)
    conf_value = forms.CharField(required=False)
    description = forms.CharField(required=False)
    setId = forms.IntegerField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        conf_key = cleaned_data.get("conf_key")
        conf_value = cleaned_data.get("conf_value")
        description = cleaned_data.get("description")
        setId = cleaned_data.get("setId")
        
        if not conf_key:
            msg = forms.ValidationError("This field is required.")
            self.add_error('conf_key', msg)
        if not conf_value:
            msg = forms.ValidationError("This field is required.")
            self.add_error('conf_value', msg)
        if not description:
            msg = forms.ValidationError("This field is required.")
            self.add_error('description', msg)

        type_check = DmsSetting.objects.filter(conf_key=conf_key).exclude(id=setId).count()
        if type_check:
            msg = forms.ValidationError("Sorry! Settings already exist.")
            self.add_error('conf_key', msg)

class SaveCountry(forms.Form): # pylint: disable=too-few-public-methods
    """Save Country"""
    txt_name = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        txt_name = cleaned_data.get("txt_name")
        
        if not txt_name:
            msg = forms.ValidationError("This field is required.")
            self.add_error('txt_name', msg)

        type_check = Country.objects.filter(name=txt_name).count()
        if type_check:
            msg = forms.ValidationError("Sorry! Country already exist.")
            self.add_error('txt_name', msg)

class UpateCountry(forms.Form): # pylint: disable=too-few-public-methods
    """Save Country"""
    txt_name = forms.CharField(required=False)
    typeid = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        txt_name = cleaned_data.get("txt_name")
        typeid = cleaned_data.get("typeid")
        
        if not txt_name:
            msg = forms.ValidationError("This field is required.")
            self.add_error('txt_name', msg)

        type_check = Country.objects.filter(name=txt_name).exclude(id=typeid).count()
        if type_check:
            msg = forms.ValidationError("Sorry! Country already exist.")
            self.add_error('txt_name', msg)

class SaveState(forms.Form): # pylint: disable=too-few-public-methods
    """Save State"""
    txt_name = forms.CharField(required=False)
    country = forms.IntegerField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        txt_name = cleaned_data.get("txt_name")
        country = cleaned_data.get("country")
        
        if not country:
            msg = forms.ValidationError("This field is required.")
            self.add_error('country', msg)

        if not txt_name:
            msg = forms.ValidationError("This field is required.")
            self.add_error('txt_name', msg)

        type_check = State.objects.filter(name=txt_name,country=country).count()
        if type_check:
            msg = forms.ValidationError("Sorry! State already exist.")
            self.add_error('txt_name', msg)

class UpdateState(forms.Form): # pylint: disable=too-few-public-methods
    """Save State"""
    txt_name = forms.CharField(required=False)
    country = forms.IntegerField(required=False)
    typeid = forms.IntegerField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        txt_name = cleaned_data.get("txt_name")
        country = cleaned_data.get("country")
        typeid = cleaned_data.get("typeid")
        
        if not country:
            msg = forms.ValidationError("This field is required.")
            self.add_error('country', msg)

        if not txt_name:
            msg = forms.ValidationError("This field is required.")
            self.add_error('txt_name', msg)

        type_check = State.objects.filter(name=txt_name,country=country).exclude(id=typeid).count()
        if type_check:
            msg = forms.ValidationError("Sorry! State already exist.")
            self.add_error('txt_name', msg)
class SavePurposeForm(forms.Form): # pylint: disable=too-few-public-methods
    """Save Purpose Form"""
    txt_name = forms.CharField(required=False)
    def clean(self):
        cleaned_data = super().clean()
        txt_name = cleaned_data.get("txt_name")
        
        if not txt_name:
            msg = forms.ValidationError("This field is required.")
            self.add_error('txt_name', msg)

        type_check = DronePurpose.objects.filter(name=txt_name).count()
        if type_check:
            msg = forms.ValidationError("Sorry! Drone Purpose already exist.")
            self.add_error('txt_name', msg)

class UpdatePurposeForm(forms.Form): # pylint: disable=too-few-public-methods
    """Save Purpose Form"""
    txt_name = forms.CharField(required=False)
    purpId = forms.IntegerField(required=False)
    def clean(self):
        cleaned_data = super().clean()
        txt_name = cleaned_data.get("txt_name")
        purpId = cleaned_data.get("purpId")
        
        if not txt_name:
            msg = forms.ValidationError("This field is required.")
            self.add_error('txt_name', msg)

        type_check = DronePurpose.objects.filter(name=txt_name).exclude(id=purpId).count()
        if type_check:
            msg = forms.ValidationError("Sorry! Drone Purpose already exist.")
            self.add_error('txt_name', msg)

class SaveDroneTypeForm(forms.Form): # pylint: disable=too-few-public-methods
    """Save Drone Type Form"""
    txt_name = forms.CharField(required=False)
    purpose = forms.IntegerField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        txt_name = cleaned_data.get("txt_name")
        purpose = cleaned_data.get("purpose")
        
        if not txt_name:
            msg = forms.ValidationError("This field is required.")
            self.add_error('txt_name', msg)
        if not purpose:
            msg = forms.ValidationError("This field is required.")
            self.add_error('purpose', msg)

        type_check = DroneType.objects.filter(name=txt_name,purpose=purpose).count()
        if type_check:
            msg = forms.ValidationError("Sorry! Drone Type already exist.")
            self.add_error('txt_name', msg)
class UpdateDroneTypeForm(forms.Form): # pylint: disable=too-few-public-methods
    """Save Drone Type Form"""
    txt_name = forms.CharField(required=False)
    purpose = forms.IntegerField(required=False)
    typeid = forms.IntegerField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        txt_name = cleaned_data.get("txt_name")
        purpose = cleaned_data.get("purpose")
        typeid = cleaned_data.get("typeid")
        
        if not txt_name:
            msg = forms.ValidationError("This field is required.")
            self.add_error('txt_name', msg)
        if not purpose:
            msg = forms.ValidationError("This field is required.")
            self.add_error('purpose', msg)

        type_check = DroneType.objects.filter(name=txt_name,purpose=purpose).exclude(id=typeid).count()
        if type_check:
            msg = forms.ValidationError("Sorry! Drone Type already exist.")
            self.add_error('txt_name', msg)


class SaveReason(forms.Form): # pylint: disable=too-few-public-methods
    """Save Reason"""
    txt_reason = forms.CharField(required=False)
    cb_module = forms.CharField(required=False)
 
    def clean(self):
        cleaned_data = super().clean()
        txt_reason = cleaned_data.get("txt_reason")
        cb_module = cleaned_data.get("cb_module")
        
        if not txt_reason:
            msg = forms.ValidationError("This field is required.")
            self.add_error('txt_reason', msg)
        if not cb_module:
            msg = forms.ValidationError("This field is required.")
            self.add_error('cb_module', msg)

        type_check = DroneStatus.objects.filter(status=txt_reason,type = cb_module).count()
        if type_check:
            msg = forms.ValidationError("Sorry! Reason already exist.")
            self.add_error('txt_reason', msg)

class UpdateReason(forms.Form): # pylint: disable=too-few-public-methods
    """Save Reason"""
    txt_reason = forms.CharField(required=False)
    cb_module = forms.CharField(required=False)
    hd_id = forms.IntegerField(required=False)
 
    def clean(self):
        cleaned_data = super().clean()
        txt_reason = cleaned_data.get("txt_reason")
        cb_module = cleaned_data.get("cb_module")
        hd_id = cleaned_data.get("hd_id")
        
        if not txt_reason:
            msg = forms.ValidationError("This field is required.")
            self.add_error('txt_reason', msg)
        if not cb_module:
            msg = forms.ValidationError("This field is required.")
            self.add_error('cb_module', msg)

        type_check = DroneStatus.objects.filter(status=txt_reason,type = cb_module).exclude(id=hd_id).count()
        if type_check:
            msg = forms.ValidationError("Sorry! Reason already exist.")
            self.add_error('txt_reason', msg)
