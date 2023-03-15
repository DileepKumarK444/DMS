"""
Master Model
"""
# pylint: disable=E0401

from django.db import models
from django.contrib.auth.models import User
from drone_management.models import Drone,DroneStatus

TYP = (
    ("Battery", "Battery"),
    ("Sensor", "Sensor"),
    ("Camera", "Camera"),
    ("RC", "RC"),
)

TRANS_TYP = (
    ("New", "New"),
    ("Allocated", "Allocated"),
    ("Danaged", "Danaged"),
)

ACTION = (
    ("add","add"),
    ("edit","edit"),
    ("delete","delete")
)

class Company(models.Model): # pylint: disable=too-few-public-methods
    """Company Model"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    description = models.TextField(null=False)
    user = models.ForeignKey(User, default='',null=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta: # pylint: disable=too-few-public-methods
        """Company Model Meta"""
        db_table = "dms_company"
    def __str__(self):
        return f"{self.name}"

class Country(models.Model): # pylint: disable=too-few-public-methods
    """Country Model"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    description = models.TextField(null=False)
    user = models.ForeignKey(User, default='',null=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta: # pylint: disable=too-few-public-methods
        """Country Model Meta"""
        db_table = "dms_country"
    def __str__(self):
        return f"{self.name}"

class State(models.Model): # pylint: disable=too-few-public-methods
    """State Model"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    description = models.TextField(null=False)
    country = models.ForeignKey(Country, default='',null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, default='',null=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta: # pylint: disable=too-few-public-methods
        """State Model Meta"""
        # unique_together = ('name', 'country',)
        db_table = "dms_state"
    def __str__(self):
        return f"{self.name}"

class Designation(models.Model): # pylint: disable=too-few-public-methods
    """Designation Model"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    description = models.TextField(null=False)
    user = models.ForeignKey(User, default='',null=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta: # pylint: disable=too-few-public-methods
        """Designation Model Meta"""
        db_table = "dms_designation"
    def __str__(self):
        return f"{self.name}"

class Customer(models.Model): # pylint: disable=too-few-public-methods
    """Customer Model"""
    id = models.AutoField(primary_key=True)
    customer_id = models.CharField(max_length=80, default="")
    account_name = models.CharField(max_length=40)
    email = models.CharField(max_length=80, default="")
    phone = models.CharField(max_length=80, default="")
    activation_date = models.DateField(null=True)
    address = models.TextField(null=False)
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE)
    state = models.ForeignKey(State, null=True, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, null=True, on_delete=models.CASCADE)
    designation = models.ForeignKey(Designation, null=True, on_delete=models.CASCADE)
    description = models.TextField(null=False)
    status = models.BooleanField(default=False)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta: # pylint: disable=too-few-public-methods
        """Customer Model Meta"""
        db_table = "dms_customers"
    def __str__(self):
        return f"{self.id}"

class CustomerUser(models.Model): # pylint: disable=too-few-public-methods
    """Customer User Model"""
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.CharField(max_length=80, default="")
    phone = models.CharField(max_length=80, default="")
    status = models.BooleanField(default=True)
    pilot = models.BooleanField(default=False)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    pilot_license = models.CharField(max_length=80, default="")
    pilot_license_file  = models.FileField(upload_to ='license_uploads/', null = True, blank = True)
    profile_image  = models.FileField(upload_to ='Profile_images/', null = True, blank = True)
    additional_fields = models.TextField(null=True,default="")
    description = models.CharField(max_length=80, default="")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta: # pylint: disable=too-few-public-methods
        """Customer User Model Meta"""
        db_table = "dms_customers_users"
    def __str__(self):
        return f"{self.id}"

class Profile(models.Model): # pylint: disable=too-few-public-methods
    """Profile Model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.TextField(blank=True)
    time_zone = models.CharField(max_length=150, null=True, default=None)
    created_on = models.DateTimeField(auto_now=True)

    class Meta: # pylint: disable=too-few-public-methods
        """Profile Model Meta"""
        db_table = "dms_user_profiles"

class Project(models.Model): # pylint: disable=too-few-public-methods
    """Project Model"""
    id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=80, default="")
    mission_commander = models.ForeignKey(CustomerUser, null=True, on_delete=models.CASCADE)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta: # pylint: disable=too-few-public-methods
        """Project Model Meta"""
        db_table = "dms_project"
    def __str__(self):
        return f"{self.id}"

class DmsSetting(models.Model): # pylint: disable=too-few-public-methods
    """Setting Model"""
    id = models.AutoField(primary_key=True)
    conf_key = models.TextField(null=False)
    conf_value = models.TextField(null=False)
    conf_description = models.TextField(null=False)

    class Meta: # pylint: disable=too-few-public-methods
        """Settings Model Meta"""
        db_table = "dms_settings"
    def __str__(self):
        return f"{self.conf_key}"

class DmsBuildLog(models.Model): # pylint: disable=too-few-public-methods
    """Build Log Model"""
    id = models.AutoField(primary_key=True)
    build_no = models.CharField(max_length=80, default="")
    build_date = models.DateTimeField(auto_now_add=True)
    portal = models.CharField(max_length=80, default="")

    class Meta: # pylint: disable=too-few-public-methods
        """Build Log Model Meta"""
        db_table = "dms_build_log"
    def __str__(self):
        return f"{self.id}"

class Pilot(models.Model): # pylint: disable=too-few-public-methods
    """Pilot Model"""
    id = models.AutoField(primary_key=True)
    first_name = models.TextField(null=False)
    last_name = models.TextField(null=False)
    phone = models.TextField(null=False)
    email = models.TextField(null=False)
    pilot_license  = models.FileField(upload_to ='license_uploads/', null = True, blank = True)
    expiry_date = models.DateField(null=True)
    status = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    customer_id = models.CharField(max_length=80, default="")

    class Meta: # pylint: disable=too-few-public-methods
        """Pilot Model Meta"""
        db_table = "dms_pilot"

class Plan(models.Model): # pylint: disable=too-few-public-methods
    """Plan Model"""
    id = models.AutoField(primary_key=True)
    plan = models.CharField(max_length=80, default="")
    pilot = models.ForeignKey(CustomerUser, null=True, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, null=True, on_delete=models.CASCADE)
    drone = models.ForeignKey(Drone, null=True, on_delete=models.CASCADE)
    plan_date = models.DateField(null=True)
    start_time = models.TimeField(auto_now=False, auto_now_add=False,null=True)
    end_time = models.TimeField(auto_now=False, auto_now_add=False,null=True)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    plan_file = models.FileField(upload_to='plan_files/',null = True, blank = True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta: # pylint: disable=too-few-public-methods
        """Plan Model Meta"""
        db_table = "dms_plan"
    def __str__(self):
        return f"{self.id}"

class DroneAllocation(models.Model): # pylint: disable=too-few-public-methods
    """Drone Allocation Model"""
    id = models.AutoField(primary_key=True)
    drone = models.ForeignKey(Drone, null=True, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta: # pylint: disable=too-few-public-methods
        """Drone Allocation Model Meta"""
        db_table = "dms_drone_allocation"
    def __str__(self):
        return f"{self.id}"

class Checklist(models.Model): # pylint: disable=too-few-public-methods
    """Checklist Model"""
    id = models.AutoField(primary_key=True)
    plan = models.ForeignKey(Plan, null=True, on_delete=models.CASCADE)
    schema = models.TextField(null=False)
    type = models.CharField(max_length=80, default="")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    class Meta: # pylint: disable=too-few-public-methods
        """Checklist Model Meta"""
        db_table = "dms_checklist"
    def __str__(self):
        return f"{self.name}"

class PlanLog(models.Model): # pylint: disable=too-few-public-methods
    """Plan Log Model"""
    id = models.AutoField(primary_key=True)
    plan = models.ForeignKey(Plan, null=True, on_delete=models.CASCADE)
    log_file = models.FileField(upload_to='plan_logs/',null = True, blank = True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta: # pylint: disable=too-few-public-methods
        """Plan Log Model Meta"""
        db_table = "dms_plan_logs"
    def __str__(self):
        return f"{self.plan}"

class PlanReport(models.Model): # pylint: disable=too-few-public-methods
    """Plan Report Model"""
    id = models.AutoField(primary_key=True)
    log = models.ForeignKey(PlanLog, null=True, on_delete=models.CASCADE)
    air_speed = models.TextField(null=False)
    flight_time = models.TextField(null=False)
    altitude_relative = models.TextField(null=False)
    battery_consumed_max = models.CharField(max_length=80, default="")
    distance_to_gcs_max = models.CharField(max_length=80, default="")
    flight_distance_max = models.CharField(max_length=80, default="")
    flight_time_max = models.CharField(max_length=80, default="")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta: # pylint: disable=too-few-public-methods
        """Plam Report Model Meta"""
        db_table = "dms_plan_reports"
    def __str__(self):
        return f"{self.log}"

class DashboardData(models.Model): # pylint: disable=too-few-public-methods
    """Dashboard Data Model"""
    id = models.AutoField(primary_key=True)
    distance = models.CharField(max_length=80, default="")
    flying_time = models.CharField(max_length=80, default="")
    plans = models.CharField(max_length=80, default="")
    gc_con_status = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    drone = models.ForeignKey(Drone, null=True, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    error_count = models.IntegerField(default=0,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta: # pylint: disable=too-few-public-methods
        """Dashboard Data Model Meta"""
        db_table = "dms_dashboard_datas"
    def __str__(self):
        return f"{self.id}"

class ProductType(models.Model): # pylint: disable=too-few-public-methods
    """Product Type Model"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80, null=True,blank=True)
    description = models.TextField(blank=True,null=True)
    active = models.BooleanField(default=False)
    type = models.CharField(max_length=80, choices=TYP, default='Battery',blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta: # pylint: disable=too-few-public-methods
        """Product Type Model Meta"""
        db_table = "dms_product_types"
    def __str__(self):
        return f"{self.id}"

class Category(models.Model): # pylint: disable=too-few-public-methods
    """Category Model"""
    id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=80, blank=True,null=True)
    type = models.ForeignKey(ProductType, null=True, on_delete=models.CASCADE,blank=True)
    additional_feature = models.CharField(max_length=80, default="",null=True)
    warranty_period = models.IntegerField(null=True)
    warranty = models.BooleanField(default=False)
    quantity = models.IntegerField(blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta: # pylint: disable=too-few-public-methods
        """Category Model Meta"""
        db_table = "dms_categories"
    def __str__(self):
        return f"{self.id}"

class Product(models.Model): # pylint: disable=too-few-public-methods
    """Product Model"""
    id = models.AutoField(primary_key=True)
    serial_number = models.CharField(max_length=80, default="")
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    trans_type = models.CharField(max_length=10, choices=TRANS_TYP, default='New')
    pur_date = models.DateField(null=True)
    warranty_start_date = models.DateField(null=True)
    warranty_end_date = models.DateField(null=True)
    status = models.BooleanField(default=True)
    drone_status = models.ForeignKey(
            DroneStatus, default='', null=True, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    note = models.TextField(blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta: # pylint: disable=too-few-public-methods
        """Product Model Meta"""
        db_table = "dms_products"
    def __str__(self):
        return f"{self.id}"


class TransactionLog(models.Model): # pylint: disable=too-few-public-methods
    """Transaction Log Model"""
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    type = models.ForeignKey(ProductType, null=True, on_delete=models.CASCADE)
    trans_type = models.CharField(max_length=10, choices=TRANS_TYP, default='New')
    quantity = models.IntegerField(blank=True,null=True)
    action = models.CharField(max_length=10, choices=ACTION, default='add')
    date = models.DateField(null=True)
    description = models.TextField(blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta: # pylint: disable=too-few-public-methods
        """Transaction Log Model Meta"""
        db_table = "dms_transaction_logs"
    def __str__(self):
        return f"{self.id}"

class LogTemplate(models.Model): # pylint: disable=too-few-public-methods
    """Log Template Model"""
    id = models.AutoField(primary_key=True)
    template_name = models.CharField(max_length=80, default="")
    log_fields = models.TextField(blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta: # pylint: disable=too-few-public-methods
        """Log Template Model Meta"""
        db_table = "dms_log_template"
    def __str__(self):
        return f"{self.id}"


class DroneConfiguraion(models.Model): # pylint: disable=too-few-public-methods
    """Drone Configuraion Model"""
    id = models.AutoField(primary_key=True)
    drone = models.ForeignKey(
        Drone, default='', null=True, on_delete=models.CASCADE)
    template = models.ForeignKey(
        LogTemplate, default='', null=True, on_delete=models.CASCADE)
    mac_id = models.CharField(max_length=80, default="",null=True)
    fc_id = models.CharField(max_length=80, default="",null=True)
    host = models.CharField(max_length=80, default="",null=True)
    port = models.CharField(max_length=80, default="",null=True)
    username = models.CharField(max_length=80, default="",null=True)
    password = models.CharField(max_length=80, default="",null=True)
    path = models.TextField(blank=True,null=True)
    public_key = models.TextField(blank=True,null=True)
    private_key = models.TextField(blank=True,null=True)
    token = models.TextField(blank=True,null=True)
    created_by = models.ForeignKey(User, default='', null=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta: # pylint: disable=too-few-public-methods
        """Drone Configuration Model Meta"""
        db_table = "dms_drone_configuraion"
    def __str__(self):
        return f"{self.id}"

class ConsumptionLog(models.Model): # pylint: disable=too-few-public-methods
    """Consumption Log Model"""
    id = models.AutoField(primary_key=True)
    drone = models.ForeignKey(
        Drone, default='', null=True, on_delete=models.CASCADE)
    cpu_usage = models.IntegerField(default=0,null=True)
    virtual_memory  = models.IntegerField(default=0,null=True)
    swap_memory = models.IntegerField(default=0,null=True)
    status = models.CharField(max_length=80,default="Unread",null=True)
    timestamp = models.DateTimeField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta: # pylint: disable=too-few-public-methods
        """Consumption Log Model Meta"""
        db_table = "dms_consumption_log"
    def __str__(self):
        return f"{self.id}"
