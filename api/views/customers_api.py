from django.utils import timezone
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework import serializers, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from django.contrib.auth import authenticate
import json
from django.contrib.auth.models import User
from utils import helper
import datetime
from masters.models import Customer, CustomerUser
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
import os
from os.path import exists
from masters.models import DmsSetting, PlanReport
from django.core.mail import send_mail
from django.template import loader
from userpermissions.models import RoleModel, UserRoleModel
from django.conf import settings
from utils.encryption import aes
import base64
import logging
from dms.serializer import CustomerUserSerializer , PlanReportSerializer
from dms.authentication import SessionTokenAuthentication
from dms.permission import CustomPermission

encry = aes(settings.KEY, settings.IV)
ROOT_DIR = os.path.abspath(os.curdir)
BASE_URL = settings.BASE_URL
APP_NAME = settings.APP_NAME

logger = logging.getLogger(__name__)

@api_view(['GET'])
# @csrf_exempt
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
@authentication_classes([SessionTokenAuthentication])
@permission_classes([CustomPermission])
def UserCustomerDetails(request):
    customer = CustomerUser.objects.filter(email=request.email).values("id","first_name","last_name","email","phone","status","pilot", "pilot_license", "description","profile_image","pilot_license_file")
    data = ''
    if(customer[0]['profile_image']):
        path = (ROOT_DIR+'/attachments/'+customer[0]['profile_image'])
        file_exists = exists(path)
        if(file_exists):
            with open(path, 'rb') as f:
                data = (base64.b64encode(f.read()))
    return Response({'data':data,'customer':customer})

@api_view(['POST'])
@csrf_exempt
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
@authentication_classes([SessionTokenAuthentication])
@permission_classes([CustomPermission])
def UserCustomerSave(request):
    _cust_id = ''
    try:
        _cust_id = helper.get_customer_id(request)
        data = request.data
        file =''
        if(request.FILES.get('file')):
            file = (request.FILES.get('file'))
        cust_id = request.customer_id
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        phone = data['phone']
        pilot = data['pilot']
        additional_fields = data['profile_schema_model']
        if(pilot=='true'):
            pilot=True
        else:
            pilot=False
        pilot_license = data['pilot_license']
        description = data['description']
        customer_id = cust_id[0] 
        active = False
        customer_idno = Customer.objects.get(customer_id=cust_id[0])
        usercount = CustomerUser.objects.filter(customer = customer_idno).count()
        userlimit = DmsSetting.objects.filter(conf_key='userlimit').values('conf_value')
        if usercount >= int(userlimit[0]['conf_value']):
            msg = helper.get_customer_details(_cust_id,'Sorry! User limit exceeded.')
            logger.info(msg)
            return Response({'success': 'exist', 'msg': 'Sorry! User limit exceeded.'})
        email_check = CustomerUser.objects.filter(email=email).count()
        if email_check:
            msg = helper.get_customer_details(_cust_id,'Sorry! email already exist.')
            logger.info(msg)
            return Response({'success': 'exist', 'msg': 'Sorry! email already exist.'})
        password = helper.generate_password()
        user_data = User(
            first_name=first_name,
            last_name=last_name,
            username=email,
            email=email,
            is_superuser=False,
            is_staff=False,
            is_active=False,
            date_joined=datetime.datetime.now(tz=timezone.utc)
        )

        user_data.set_password(password)
        user_data.save()
        user_id = User.objects.latest('id')
        user = User.objects.get(email=email)
        cust_id = Customer.objects.get(customer_id=customer_id)
        customer = CustomerUser(
            first_name=first_name,
            last_name = last_name,
            email = email,
            phone = phone,
            status = active,
            user=user,
            customer = cust_id,
            pilot = pilot,
            pilot_license = pilot_license,
            description = description,
            pilot_license_file=file,
            additional_fields = additional_fields
        )
        customer.save()
        cust_user = CustomerUser.objects.latest('id')
        encryptData = encry.encrypt(str(cust_user.id))
        encryptData = encryptData.replace("/", "$$$")
        email_verification =list(DmsSetting.objects.filter(conf_key='email_verification_user').values_list('conf_value', flat = True))
        if(email_verification[0] == 'True'):
            t  = datetime.datetime.now()
            encrypt_t = encry.encrypt(str(t))
            encrypt_t = encrypt_t.replace("/", "$$$")
            subject = "Email Verification"
            end_url = f"{BASE_URL}/masters/verify_email/"+encryptData+"/"+encrypt_t+"/"
            html_message = loader.render_to_string('etl/email/user_template.html',
                                                {'app_name': APP_NAME, 'name': first_name,'first_name':email,'password':password,'end_url':end_url,'BASE_URL':BASE_URL})
            send_mail(subject, '', APP_NAME + ' <do_not_reply@domain.com>', [
            email], fail_silently=False, html_message=html_message)
        else:
            customer_user = CustomerUser.objects.get(id=cust_user.id)
            customer_user.status = True
            customer_user.save()
            user = User.objects.get(id=user_id.id)
            user.is_active = True
            user.save()
        role_data = RoleModel.objects.get(name='Customer User')
        user_role = UserRoleModel()
        user_role.role_id = role_data
        user_role.user_id = user_data
        user_role.save()
        if os.path.exists(ROOT_DIR + "/customer_list") == False:
            os.mkdir(ROOT_DIR + "/customer_list")
        f = open(ROOT_DIR + "/customer_list/"+first_name+".txt", "w")
        f.write("Username : "+email+" \nPassword : "+password)
        f.close()
        return Response({'success': 'true', 'msg': 'User created successfully.','password':password},status=200)
    except Exception as e:
        msg = helper.get_customer_details(_cust_id,str(e))
        logger.info(msg)
        return Response({'success': 'false', 'msg': str(e)},status=500)

@api_view(['POST'])
@csrf_exempt
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
@authentication_classes([SessionTokenAuthentication])
@permission_classes([CustomPermission])
def GetUserList(request):
    data = json.loads(request.body)
    cust_id = request.customer_id
    customer_id = Customer.objects.get(customer_id=cust_id[0])
    check_if_subuser_exists = Customer.objects.filter(customer_id = cust_id[0]).count()
    if check_if_subuser_exists:
        customer = CustomerUser.objects.filter(customer = customer_id,user__in=User.objects.filter(is_active=True)).values("id","first_name", "last_name", "email", "pilot", "phone") 
    return Response(customer)

@api_view(['POST'])
@csrf_exempt
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
@authentication_classes([SessionTokenAuthentication])
@permission_classes([CustomPermission])
def CustomerSave(request):
    _cust_id = ''
    try: 
        _cust_id = helper.get_customer_id(request)
        print("_custid",_cust_id)
        data = json.loads(request.body)
        account_name = data['account_name']
        print("account",account_name)
        email = data['email']
        phone = data['phone']
        customer_id = data['customer_id']
        print("customerid",customer_id)
        active = True
        activation_date = data['activation_date']
        cust_id_check = Customer.objects.filter(customer_id=customer_id).count()
        if cust_id_check:
            msg = helper.get_customer_details(_cust_id,'Sorry! Customer ID already exist.')
            logger.info(msg)
            return Response({'success': 'exist', 'msg': 'Sorry! Customer ID already exist.'})
        email_check = Customer.objects.filter(email=email).count()
        if email_check:
            msg = helper.get_customer_details(_cust_id,'Sorry! email already exist.')
            logger.info(msg)
            return Response({'success': 'exist', 'msg': 'Sorry! email already exist.'})
        customer = Customer(
            account_name=account_name,
            email = email,
            phone = phone,
            status = active,
            customer_id = customer_id,
            activation_date = activation_date
        )
        customer.save()
        encryptData = encry.encrypt(customer_id)
        encryptData = encryptData.replace("/", "$$$")
        url = BASE_URL+'/masters/customers_admin/'+encryptData
        return Response({'success': 'true', 'msg': 'Customer created successfully.','url':url},status=200)
    except Exception as e:
        msg = helper.get_customer_details(_cust_id,'Sorry! error on customer save')
        logger.info(msg)
        return Response({'success': 'false', 'msg': 'Sorry! error on customer save'},status=500)

@api_view(['POST'])
@csrf_exempt
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
@authentication_classes([SessionTokenAuthentication])
@permission_classes([CustomPermission])
def GetSelectedUserDetails(request):
    data = json.loads(request.body)
    cust_id = request.customer_id
    _id = data['id']
    profile_schema = DmsSetting.objects.filter(conf_key='profile_schema').values('conf_value')
    check_if_subuser_exists = Customer.objects.filter(customer_id = cust_id[0]).count()
    if check_if_subuser_exists:
        customer = CustomerUser.objects.filter(id = _id).values("id","first_name", "last_name", "email", "pilot", "phone", "pilot_license", "description","pilot_license_file","additional_fields") 
    return Response({'customer':customer,'profile_schema':profile_schema})

@api_view(['POST'])
@csrf_exempt
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
@authentication_classes([SessionTokenAuthentication])
@permission_classes([CustomPermission])
def UserCustomerUpdate(request):
    _cust_id =''
    try:
        _cust_id = helper.get_customer_id(request)
        data = request.data
        file =''
        if(request.FILES.get('file')):
            file = (request.FILES.get('file'))
        pilot = data['pilot']
        if(pilot=='true'):
            pilot=True
        else:
            pilot=False
        cust_id = request.customer_id
        _id = data['id']
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        phone = data['phone']
        pilot_license = data['pilot_license']
        description = data['description']
        additional_fields = data['profile_schema_model']
        customer_id = cust_id[0] 
        cust_id = Customer.objects.get(customer_id=customer_id)
        email_check = CustomerUser.objects.filter(email=email).exclude(id=_id).count()
        if email_check:
            msg = helper.get_customer_details(_cust_id,'Sorry! email already exist.')
            logger.info(msg)
            return Response({'success': 'exist', 'msg': 'Sorry! email already exist.'})
        customer = CustomerUser.objects.get(id = _id)
        customer.first_name = first_name
        customer.last_name = last_name
        customer.email = email
        customer.phone = phone
        customer.pilot = pilot
        customer.pilot_license = pilot_license
        customer.description = description
        if(file):
            customer.pilot_license_file=file
        customer.additional_fields = additional_fields
        customer.save()
        user = User.objects.get(id = customer.user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        cust = CustomerUser.objects.filter(id = _id).values('pilot_license_file')
        return Response({'success': 'true', 'msg': 'User updated successfully.','file':cust[0]['pilot_license_file']},status=200)
    except Exception as e:
        msg = helper.get_customer_details(_cust_id,'Sorry! error on user update')
        logger.info(msg)
        return Response({'success': 'false', 'msg': 'Sorry! error on user update'},status=200)

@api_view(['POST'])
@csrf_exempt
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
@authentication_classes([SessionTokenAuthentication])
@permission_classes([CustomPermission])
def DeleteUser(request):
    _cust_id = ''
    try:
        _cust_id = helper.get_customer_id(request)
        data = json.loads(request.body)
        _id = data['id']
        customer = CustomerUser.objects.get(id = _id)
        user = User.objects.filter(id = customer.user_id).update(is_active=False)
        return Response({'success': 'true', 'msg': 'User deleted successfully.'},status=200)
    except Exception as e:
        msg = helper.get_customer_details(_cust_id,'Sorry!, error on user deleted.')
        logger.info(msg)
        return Response({'success': 'false', 'msg': 'Sorry!, error on user deleted.'},status=200)

class ApiUserView(ListAPIView):
    def get(self, request, format=None):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        data = json.loads(self.request.body)
        cust_id = self.request.customer_id
        customer_id = Customer.objects.get(customer_id=cust_id[0])
        person_objects = CustomerUser.objects.filter(customer = customer_id)
        result_page = paginator.paginate_queryset(person_objects, request)
        serializer = CustomerUserSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
@authentication_classes([SessionTokenAuthentication])
@permission_classes([CustomPermission])
def ApiLogView(request):
    data = (request.data)
    per_page = (request.query_params.get('offset'))
    cust_id = request.customer_id
    paginator = PageNumberPagination()
    paginator.page_size = int(per_page)
    person_objects = PlanReport.objects.filter()
    person_objects = person_objects.filter(log__plan__drone=data['drone_id'],log__plan__customer = Customer.objects.filter(customer_id=cust_id[0]).first().id).order_by('-created_on')
    if(data['drone_id'] !=''):
        person_objects = person_objects.filter(log__plan__plan__icontains=data['filter']) | person_objects.filter(log__plan__project__project_name__icontains=data['filter']) | person_objects.filter(log__plan__plan_date__icontains=data['filter']) | person_objects.filter(log__plan__start_time__icontains=data['filter']) | person_objects.filter(log__plan__end_time__icontains=data['filter']) | person_objects.filter(flight_distance_max__icontains=data['filter']) | person_objects.filter(flight_time_max__icontains=data['filter'])
    if (data['plan'] != '0'):
        person_objects = person_objects.filter(log__plan__id=data['plan'])
    if (data['project'] != '0'):
        person_objects = person_objects.filter(log__plan__project__id=data['project'])
    if (data['date_from'] != ''):
        date_from = datetime.datetime.strptime(str(data['date_from']), '%Y-%m-%d')
        person_objects = person_objects.filter(log__plan__plan_date__gte=date_from)
    if (data['date_to'] != ''):
        date_to = datetime.datetime.strptime(str(data['date_to']), '%Y-%m-%d')
        person_objects = person_objects.filter(log__plan__plan_date__lte=date_to)
    if (data['time_from'] != ''):
        time_from = datetime.datetime.strptime(str(data['time_from']), '%H:%M:%S')
        person_objects = person_objects.filter(log__plan__start_time__gte=time_from)
    if (data['time_to'] != ''):
        time_to = datetime.datetime.strptime(str(data['time_to']), '%H:%M:%S')
        person_objects = person_objects.filter(log__plan__end_time__lte=time_to)
    result_page = paginator.paginate_queryset(person_objects, request)
    serializer = PlanReportSerializer(result_page, many=True)  # MAIN CHANGE IS HERE
    return paginator.get_paginated_response(serializer.data)