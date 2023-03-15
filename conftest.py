# pylint: disable=no-member
"""
GET APIs Testing
"""
from sre_parse import CATEGORIES
import pytest
from django.contrib.auth.models import User
from masters.models import Company,Country, State,Plan, ProductType,Designation,Customer,CustomerUser, DroneConfiguraion, DroneAllocation,DashboardData,DmsSetting,PlanLog,Category,Product
from drone_management.models import DroneComponent, DronePurpose,Drone, DroneType
from mixer.backend.django import mixer
import requests
import json
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
import csv 
import io
import pytz
# import mock
from django.core.files import File
import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
from os.path import exists
import tempfile
from masters.models import DmsSetting
from userpermissions.models import  UserRoleModel, GroupPermissionModel, RoleGroupModel, RoleModel, GroupModel,PermissionModel

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user_2(db):
    user2 =  User.objects.create_user(username='dileep@gmail.com', password='password',is_superuser=True)
    return user2

@pytest.fixture
def user_3(db):
    # user4 =  User.objects.create_user(pk=2,username='dileep@gmail.com', password='password',email='dileep@gmail.com')
    user3 =  User.objects.create(username='dileep@gmail.com', password='password',email='dileep@gmail.com')
    print('user3',user3)
    return user3

@pytest.fixture(scope='function')
def authorization_token(db,user_3):

    
    plan =  mixer.blend(Plan,user=user_3)
    role = mixer.blend(RoleModel,name='Customer User') 
    group = mixer.blend(GroupModel)
    permission = mixer.blend(PermissionModel)
    company =  mixer.blend(Company,user_id=user_3.id)
    print('company',company.user.id)
    user_4 =User.objects.get(id= user_3.id)
    mixer.blend(UserRoleModel,user_id_id=user_4.id,role_id=role)
    mixer.blend(RoleGroupModel,role_id=role,group_id=group)
    mixer.blend(GroupPermissionModel,group_id=group,permission_id=permission)
    drone = mixer.blend(Drone,image='',image1='',image2='')
    
    typ1 =mixer.blend(ProductType,name='FC',type='Flight Controller')
    typ2 =mixer.blend(ProductType,name='QGC',type='QGC')
    typ3 =mixer.blend(ProductType,name='Action Camera',type='Camera')
    typ4 =mixer.blend(ProductType,name='Lithium polymer',type='Battery')
    typ5 =mixer.blend(ProductType,name='Gyroscopes',type='Sensors')
    typ6 =mixer.blend(ProductType,name='Octa Frames',type='Frames')
    typ7 =mixer.blend(ProductType,name='Stand Alone',type='Remote Control')
    
    cat1 =mixer.blend(Category,model='FC001',type=typ1)
    cat2 =mixer.blend(Category,model='QGC001',type=typ2)
    cat3 =mixer.blend(Category,model='Action Camera001',type=typ3)
    cat4 =mixer.blend(Category,model='Lithium polymer001',type=typ4)
    cat5 =mixer.blend(Category,model='Gyroscopes001',type=typ5)
    cat6 =mixer.blend(Category,model='Octa Frames001',type=typ6)
    cat7 =mixer.blend(Category,model='Stand Alone001',type=typ7)

    prod1 =mixer.blend(Product,serial_no='FC001',category=cat1)
    prod2 =mixer.blend(Product,serial_no='QGC001',category=cat2)
    prod3 =mixer.blend(Product,serial_no='Action Camera001',category=cat2)
    prod4 =mixer.blend(Product,serial_no='Lithium polymer001',category=cat2)
    prod5 =mixer.blend(Product,serial_no='Gyroscopes001',category=cat2)
    prod6 =mixer.blend(Product,serial_no='Octa Frames001',category=cat2)
    prod7 =mixer.blend(Product,serial_no='Stand Alone001',category=cat2)


    mixer.blend(DroneComponent,battery=[str(prod4.id)],camera=[str(prod3.id)],drone_id=drone.id,sensors=[str(prod5.id)],fc=[str(prod1.id)],frame=[str(prod6.id)],qgc=[str(prod2.id)])


    
    mixer.blend(DroneComponent,drone_id=drone.id)
    country1 = mixer.blend(Country,user_id=user_3.id)
    state1 = mixer.blend(State,country_id=country1.id,user_id=user_3.id)
    desg = mixer.blend(Designation,user_id=user_3.id)
    
    customer = Customer.objects.create(customer_id='DMS00001',company_id=company.id,designation=desg,country=country1,state_id=state1.id)
    print('customer',customer.state.user_id)
    mixer.blend(DroneAllocation,drone_id=drone.id,customer_id=customer.id)
    # mixer.blend(CustomerUser,user_id=user_3.id,email='dileep@gmail.com',customer_id=customer.id)
    user_id = mixer.blend(CustomerUser,user_id=user_3.id,email='dileep@gmail.com',customer_id=customer.id,pilot_license_file='license_uploads/sample.pdf')
    token = Token.objects.get_or_create(user_id=user_3.id)
    # print('drone.id',drone.id)
    return token[0],drone.id, plan,user_id.id




# @pytest.fixture
# def done_list_data():
# @pytest.fixture
# def token_return():
#     return 'Token M1e:06:48:ee:6dF0026001D 3438510A 39303535Tb81b94e570d40117bb62e0edcbf9f025aa7b13f42d3e8da3924e4b57067b9eb7'

@pytest.fixture
def token_tring():
    # DroneConfiguraion.objects.create()
    drone = mixer.blend(Drone,image='',image1='',image2='')
    customer = mixer.blend(Customer)
    mixer.blend(DroneAllocation,drone_id=drone.id,customer_id=customer.id)
    mixer.blend(DroneConfiguraion,mac_id='1e:06:48:ee:6d',fc_id='0026001D 3438510A 39303535',token='b81b94e570d40117bb62e0edcbf9f025aa7b13f42d3e8da3924e4b57067b9eb7',drone_id=drone.id)
    return 'Token M1e:06:48:ee:6dF0026001D 3438510A 39303535Tb81b94e570d40117bb62e0edcbf9f025aa7b13f42d3e8da3924e4b57067b9eb7',customer.id,drone.id

@pytest.fixture
def data_cpu():
    return{'cpu_usage':80,'virtual_memory':90,'swap_memory':40,'timestamp': datetime.datetime.now(pytz.timezone('Asia/Kolkata'))}

@pytest.fixture
def get_file(token_tring):
    mixer.blend(DroneConfiguraion,mac_id='1e:06:48:ee:6d',fc_id='0026001D 3438510A 39303535',token='b81b94e570d40117bb62e0edcbf9f025aa7b13f42d3e8da3924e4b57067b9eb7',drone_id=token_tring[2])
    plan = mixer.blend(Plan,plan='dileepstar10',drone_id=token_tring[2],customer_id=token_tring[1])
    mixer.blend(DashboardData,drone_id=token_tring[2],customer_id=token_tring[1])
    data = ''
    data1 = {
            'plan':[plan.plan],
            'file':(open('api\\tests\\2021-12-22_11-50-07_vehicle1_b8OAgRJ.csv', 'rb'),'text/csv')
        }
    return data,data1,token_tring[0]

@pytest.fixture
def get_file1(token_tring):

    cust=mixer.blend(CustomerUser)

    data1 = {
            'id':cust.id,
            'file':open('api\\tests\\AKKII.jpg', 'rb')
        }
    return data1
@pytest.fixture
def user_1(db):
    user1 =  User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK',is_superuser=True)
    return user1
@pytest.fixture
def get_user(db):
    return {'username':'dileep@gmail.com','password':'password'} 

@pytest.fixture
def login_check(db,client,user_1):
    return {'username':'testuser1','password':'1X<ISRUkw+tuK'}

@pytest.fixture
def country_data_for_save(db,client):
    return {
        "txt_name":"Sample Country",
        "description":"Sample Description"
    }

@pytest.fixture
def country_data_for_update(db,client,user_1):
    c =  mixer.blend(Country,user=user_1)
    return {
        "txt_name":"Sample Country",
        "description":"Sample Description",
        "typeid":c.id
    }
    return c

@pytest.fixture
def state_data_for_save(db,client,country_data_for_save,user_1,country):
    return {
        "txt_name":"Sample State",
        "description":"Sample Description",
        "country":country.id,
        "user":user_1.id
    }
@pytest.fixture
def drone_type_data_for_save(db,client):
    c =  mixer.blend(DronePurpose)
    return {
        "name":"Sample Drone Type",
        "description":"Sample Drone Type Description",
        "purpose":c.id,
        "active":True
    }
@pytest.fixture
def drone_type(db,client):
    p = mixer.blend(DronePurpose)
    c =  mixer.blend(DroneType,purpose_id=p.id)

    return {'id':p.id}

@pytest.fixture
def state_data_for_update(db,client,user_1,country):
    c =  mixer.blend(State,user=user_1)
    return {
        "txt_name":"Sample State1",
        "description":"Sample Description",
        "country":country.id,
        "user":user_1.id,
        "typeid":c.id
    }

@pytest.fixture()
def company(db,user_1):
    c =  mixer.blend(Company,user=user_1)
    return c
@pytest.fixture()
def product_type(db,user_1):
    c =  mixer.blend(ProductType)
    return c

@pytest.fixture
def country(db,user_1):
    c = Country.objects.create(name = "Country1",description="Country description",user=user_1)
    return c

@pytest.fixture()
def state(db,user_1,country):
    c =  mixer.blend(State,user=user_1,country=country)
    return c
@pytest.fixture
def designation(db,user_1):
    c =  mixer.blend(Designation,user=user_1)
    return c
@pytest.fixture
def customer_save_data(company,country,state,designation,user_1):
    return {
        "first_name" : "Sample Customer",
        "email" : "sample@gmail.com",
        "phone" : "9874556622",
        "activation_date":"2022-05-20",
        "description":"Sample escription",
        "address":"Sample address",
        "active":True,
        "company":company.id,
        "country":country.id,
        "state":state.id,
        "designation":designation.id,
        "user":user_1.id

    }

@pytest.fixture
def supply_url():
	return "http://127.0.0.1:8006/api"
@pytest.fixture
def get_token(supply_url):
    url = supply_url+'/token-auth/'
    data = {'username':'dileep@gmail.com','password':'password'}
    resp = requests.post(url, json=data)
    # token = json.loads(get_token)
    return json.loads(resp.text)

# @pytest.fixture
# def get_token(get_token):
#     return {'Content-Type': "application/json", 'Accept': "application/json","Authorization":"Token "+get_token['token']}

@pytest.fixture
def get_headers(get_token):
    return {'Content-Type': "application/json", 'Accept': "application/json","Authorization":"Token "+get_token['token']}

@pytest.fixture
def get_new_token():
    return 'Token b81b94e570d40117bb62e0edcbf9f025aa7b13f42d3e8da3924e4b57067b9eb7'

@pytest.fixture
def get_drone_id():
    return 1

@pytest.fixture
def get_plan_id():
    return 1
@pytest.fixture
def get_new_headers(get_new_token):
    return {'Content-Type': "application/json", 'Accept': "application/json","AuthToken":get_new_token}

@pytest.fixture
def save_for_checklist(user_1):
    c =  mixer.blend(Plan,user=user_1)

    # print('Plan ID',c.id)
    rule_data = [{"checked_all": True, "rules": [
                {"id": 1, "val": "No Flying in Red zone", "checked": True}, 
                {"id": 2, "val": "No Flying in Adverse weather", "checked": True}]}]

    maintenance_data = [{"checked_all": True, "maintenance": [
                {"id": 3, "val": "Preflight Checking", "checked": True}, 
                {"id": 4, "val": "Location Checking", "checked": True}, 
                {"id": 5, "val": "Camera/Sensor Checking", "checked": True}]}]

    approval_data = [{"checked_all": True, "approval": [
                {"id": 6, "val": "Verified Maintanence", "checked": True}, 
                {"id": 7, "val": "Verified Location", "checked": True}, 
                {"id": 8, "val": "Verified Pilot", "checked": True}]}]

    return {
        "plan_id": c.id,
        "rule_data":rule_data,
        "maintenance_data":maintenance_data,
        "approval_data":approval_data
    }
    
@pytest.fixture
def get_report_filter_data(get_drone_id):
    return {
        "drone_id":get_drone_id,
        "filter_from_dt":'',
        "filter_to_dt":'',
        "filter_project":0,
        "filter_plan":0,
        "filter_limit":0
    }
@pytest.fixture
def get_reason_save_data(db):
    c =  mixer.blend(DmsSetting,conf_key='reason_module',conf_value=json.dumps(["Drone","Item"]))
    
@pytest.fixture
def save_data_product_type(db):
    return{
     "name":'product types',
     "description":"many products",
     "active":True,
     "type":"semi"}

@pytest.fixture
def save_data_purpose_type(db):
    return{
     "name":'product types',
     "description":"many products",
     "active":True,
     }

@pytest.fixture
def save_data_settings(db):
    return{
     "conf_key":'set1',
     "conf_value":"settings",
     
     }
@pytest.fixture   
def save_product_data(db):
    return{
        "serial_number":111,
        "trans_type":"air",
        "category_id":1,
        "drone_status_id":11,
        "status":True,
        "active":True,
        "Note":"asas"}

@pytest.fixture
def drone_type_for_updated(db,client):
    c =  mixer.blend(DronePurpose)
    return {
        "name":"Sample Drone Type",
        "description":"Sample Drone Type Description",
        "purpose":c.id,
        "active":True
    }

@pytest.fixture
def product_type_for_update(db,client):
    c =  mixer.blend(ProductType)
    return{
     "name":'product types',
     "description":"many products",
     "active":True,
     "type":"semi"}

@pytest.fixture   
def products_for_update(db,client):
    return{
        "serial_number":111,
        "trans_type":"air",
        "category_id":1,
        "drone_status_id":11,
        "status":True,
        "active":True,
        "Note":"asas"}

@pytest.fixture
def settings_for_update(db,client):
    return{
     "conf_key":'set1',
     "conf_value":"settings",
     
     }
@pytest.fixture
def purpose_for_update(db,client):
    return{
     "name":'product types',
     "description":"many products",
     "active":True,
     }

@pytest.fixture   
def save_log_field_data(db):
    return{
        "template_name":"asdf",
        "log_fields":"asaa",
        }
@pytest.fixture   
def save_category_data(db):
    return{
        "model":"asdf",
        "additional_feature":"asaa",
        "warranty_period":2,
        "warranty":True,
        "quantity":10,
        "type_id":11,
        }
@pytest.fixture   
def save_reason_data(db):
    return{
        "status":"asdf",
        "slug":"asaa",
        "type":"sasa",
        }
@pytest.fixture   
def reason_for_update(db):
    return{
        "status":"asdf",
        "slug":"asaa",
        "type":"sasa",
        }  
    
@pytest.fixture   
def category_for_update(db):
    return{
        "model":"asdf",
        "additional_feature":"asaa",
        "warranty_period":2,
        "warranty":True,
        "quantity":10,
        "type_id":11,
        }
@pytest.fixture   
def log_field_for_update(db):
    return{
        "template_name":"asdf",
        "log_fields":"asaa",
        }
@pytest.fixture
def customer_for_update(company,country,state,designation,user_1):
    return {
        "first_name" : "Sample Customer",
        "email" : "sample@gmail.com",
        "phone" : "9874556622",
        "activation_date":"2022-05-20",
        "description":"Sample escription",
        "address":"Sample address",
        "active":True,
        "company":company.id,
        "country":country.id,
        "state":state.id,
        "designation":designation.id,
        "user":user_1.id

    }
    

@pytest.fixture
def get_cust_id(db):
    customer=mixer.blend(Customer,customer_id='123')
    user_id=mixer.blend(User,password='password')
    cust_user=mixer.blend(CustomerUser,customer_id=customer.id,user_id=user_id.id,pilot_license_file='Dileep_licence.pdf')
    # print("conftest",user_id.id)
    
    return{'id':cust_user.id,

           'new_password':'asd1', 
           'password':'password'}   

@pytest.fixture
def get_cust_id2(db):
    cust=mixer.blend(CustomerUser)
    
    return{'id':cust.id,
           'new_password':'asd4', 
           'password':'password'} 

@pytest.fixture
def customer_details(db,company,country,state,designation,user_1):
    customer=mixer.blend(Customer,customer_id='123')
    user_id=mixer.blend(User,password='password')
    cust_user=mixer.blend(CustomerUser,customer_id=customer.id,user_id=user_id.id)
    # user_id = mixer.blend(CustomerUser,user_id=user_3.id,email='dileep@gmail.com',customer_id=customer.id,pilot_license_file='license_uploads/sample.pdf')
    return {
        "first_name" : "Sample Customer",
        'last_name':"last sample",
        "email" : "sample@gmail.com",
        "phone" : "9874556622",
        'profile_schema_model':'profile_schema_model',
        'pilot':True,
        'pilot_license':'license_uploads/Dileep_licence.pdf',
        "description":"Sample description",
        
        "address":"Sample address",
        "active":True,
        "company":company.id,
        "country":country.id,
        "state":state.id,
        "designation":designation.id,
        "user":user_1.id

    }
@pytest.fixture
def customer_details1(db):
    mixer.blend(DmsSetting,conf_key='userlimit',conf_value=5)
    mixer.blend(DmsSetting,conf_key='email_verification_user',conf_value='False')
    # customer=mixer.blend(Customer,customer_id=1)
    # user_id=mixer.blend(User,password='password')
    # cust_user=mixer.blend(CustomerUser,customer_id=customer.id,user_id=user_id.id,pilot_license_file='Dileep_licence.pdf')
    # # print("conftest",user_id.id)
    
    

    return{
        'id':1,
        'account_name':'sample_name',
        'file':(open('api\\tests\\download.pdf', 'rb')),
        "first_name" : "Sample Customer",
        'last_name':"last sample",
        "email" : "sample@gmail.com",
        "phone" : "9874556622",
        'profile_schema_model':'{"department":"AAAAAAAA","designation":"SSSSSSSSSSSS","organization":"QQQQQQQQQQQQ"}',
        'pilot':'true',
        'pilot_license':'12333',
        "description":"Sample description",
        'account_name':'sampleaccount',
        'activation_date':"2022-05-20",
        'customer_id':'1'
    }
@pytest.fixture
def customer_details2(db):
    mixer.blend(DmsSetting,conf_key='userlimit',conf_value=5)
    mixer.blend(DmsSetting,conf_key='email_verification_user',conf_value='False')
   
    return{
        'id':1,
        'account_name':'sample_name',
        # 'file':(open('api\\tests\\download.pdf', 'rb')),
        "first_name" : "Sample Customer",
        'last_name':"last sample",
        "email" : "sample@gmail.com",
        "phone" : "9874556622",
        # 'profile_schema_model':'{"department":"AAAAAAAA","designation":"SSSSSSSSSSSS","organization":"QQQQQQQQQQQQ"}',
        # 'pilot':'true',
        # 'pilot_license':'12333',
        # "description":"Sample description",
        # 'account_name':'sampleaccount',
        'activation_date':"2022-05-20",
        'customer_id':'1'
    }
    
@pytest.fixture
def customer_details_for_update(db):
    mixer.blend(DmsSetting,conf_key='userlimit',conf_value=5)
    mixer.blend(DmsSetting,conf_key='email_verification_user',conf_value='False')
    
    return{
        'file':(open('api\\tests\\download.pdf', 'rb')),
        "first_name" : "Sample Customer1",
        'last_name':"last sample1",
        "email" : "sample1@gmail.com",
        "phone" : "9874556623",
        'profile_schema_model':'{"department":"AAAAAAAA","designation":"SSSSSSSSSSSS","organization":"QQQQQQQQQQQQ"}',
        'pilot':'true',
        'pilot_license':'12334',
        "description":"Sample description",
        'account_name':'sampleaccount',
        'activation_date':'',
    }
@pytest.fixture
def pilot_details(db):
    customer=mixer.blend(Customer,customer_id='123')
    return{
        # 'file':(open('api\\tests\\2021-12-22_11-50-07_vehicle1_b8OAgRJ.csv', 'rb'),'text/csv'),
        "first_name" : "Sample Customer",
        'last_name':"last sample",
        "email" : "sample@gmail.com",
        "phone" : "9874556622",
        # 'profile_schema_model':'profile_schema_model',
        # 'pilot':True,
        'pilot_license':'license_uploads/Dileep_licence.pdf',
        'expiry_date':'2022-05-20',
        # "description":"Sample description",
    }

@pytest.fixture
def plan_details(db):
    mixer.blend(DmsSetting,conf_key='userlimit',conf_value=12)
    mixer.blend(DmsSetting,conf_key='email_verification_user',conf_value='False')
    customer=mixer.blend(Customer,customer_id=12)
    user_id=mixer.blend(User,password='password')
    cust_user=mixer.blend(CustomerUser,customer_id=customer.id,user_id=user_id.id,pilot_license_file='Dileep_licence.pdf')
    
    return{'file':(open('api\\tests\\dileepstar.plan', 'rb')),
         "data":{'project_name': 'project_name',
        'plan_date' : '2022-05-20',
        'start_time' : '',
        'end_time' : '',
        'first_name' : 'first_name',
        'last_name' : 'last_name',
        'plan' :'plan',
        'customer_id':'1',
        'id':1,},
        }
        
    

@pytest.fixture
def project_details(db):
    mixer.blend(DmsSetting,conf_key='userlimit',conf_value=12)
    mixer.blend(DmsSetting,conf_key='email_verification_user',conf_value='False')
    customer=mixer.blend(Customer,customer_id=12)
    user_id=mixer.blend(User,password='password')
    cust_user=mixer.blend(CustomerUser,customer_id=customer.id,user_id=user_id.id,pilot_license_file='Dileep_licence.pdf')
    # print("conftest",user_id.id)
    
    return{'id':user_id.id,
        
        'project_name': 'project name',
        'mission_commander' : 12,
        'start_date' : '2022-05-20', 
        'end_date' : '2022-05-30',
        'customer_id':12 ,
        }