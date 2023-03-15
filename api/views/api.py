from ctypes.wintypes import MSG
from fileinput import filename
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes
    )
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework import serializers, status
from django.contrib.auth import authenticate
import json
from django.contrib.auth.models import User
import datetime
from masters.models import Customer, CustomerUser
from rest_framework.permissions import IsAuthenticated
import os
import sys
import pandas
import time
from drone_management.models import Drone, DroneType
from masters.models import (
    DmsSetting,Customer,DroneAllocation,Plan,
    Checklist,PlanLog,PlanReport,Project,
    DashboardData,DroneConfiguraion,
    LogTemplate,ConsumptionLog)
from django.core import serializers
import base64
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from utils.encryption import aes
from django.template import loader
from re import sub
from userpermissions.models import  UserRoleModel, GroupPermissionModel, RoleGroupModel
from rest_framework.authtoken.models import Token
from django.db import connection
from django.db.models import F
import paramiko
from dms.authentication import SessionTokenAuthentication
from dms.permission import CustomPermission
import logging
import re
from pathlib import Path
from utils import helper
from rest_framework.pagination import PageNumberPagination
from dms.serializer import CustomerUserSerializer , PlanReportSerializer
ROOT_DIR = os.path.abspath(os.curdir)

encry = aes(settings.KEY, settings.IV)
ROOT_DIR = os.path.abspath(os.curdir)
BASE_URL = settings.BASE_URL
APP_NAME = settings.APP_NAME
EMAIL_EXPIRED_AFTER_HOUR = settings.EMAIL_EXPIRED_AFTER_HOUR

logger = logging.getLogger(__name__)

# def helper.get_customer_by_token(id,msg):
#     cust = Customer.objects.filter(id=id).values()
#     print('cust',msg+'-'+cust[0]['account_name'])
#     return cust[0]['account_name']+' - '+msg
@api_view(['GET'])
def ReadData(request):
    """ Test """
    token =''
    try:
        ConfData = DroneConfiguraion.objects.filter(
            drone_id=request.query_params.get('drone_id')
            ).values()
        if ConfData:
            mac_id = ConfData[0]['mac_id']
            filename = mac_id.replace(":", "_")
            conf_value =  DmsSetting.objects.filter(conf_key='log_file_path').values('conf_value')
            filepath = conf_value[0]['conf_value']+filename
            path = Path(filepath)
            if path.is_file():
                file = open(filepath, 'r')
                f = file.read()
                file.close()
                if not (os.stat(filepath).st_size == 0):
                    file_data = json.loads(f)
                    authentication_string = file_data['authentication_string']
                    token =authentication_string
                    check_token_exists = DroneConfiguraion.objects.filter(token=token).values()
                    cust = DroneAllocation.objects.filter(
                        drone_id=check_token_exists[0]['drone_id']
                        ).values()
                    customer = Customer.objects.filter(id=cust[0]['customer_id']).values()
                    id = CustomerUser.objects.filter(
                        user_id=User.objects.filter(id=request.user.id).first().id
                        ).values('customer_id')
                    loged_user = Customer.objects.filter(id=id[0]['customer_id']).values()
                    if customer[0]['customer_id'] == loged_user[0]['customer_id']:
                        data = file_data
                        file = open(filepath, 'r+')
                        file.truncate(0)
                    else:
                        data = ''
                    return Response({'success': True, 'data': data}, status=200)
                else:
                    return Response({'success': True, 'data': ''}, status=200)
            else:
                msg = helper.get_customer_by_token(token,'Log data not found!')
                logger.info(msg)
                return Response({'success': True, 'data': ''}, status=200)
        else:
            msg = helper.get_customer_by_token(token,'Drone configuration not found!')
            logger.info(msg)
            return Response({'success': True, 'data': ''}, status=200)
    except Exception as e:
        msg = helper.get_customer_by_token(token,str(e))
        logger.error(str(e))
        return Response({'success': False, 'msg': str(e)}, status=500)

@api_view(['GET'])
# @authentication_classes([SessionTokenAuthentication])
# @permission_classes([CustomPermission])
def getDronesList(request):
    """ Test """
    cust_id = request.customer_id
    drone = list(Drone.objects.filter(
        id__in=DroneAllocation.objects.filter(
            customer=Customer.objects.filter(
                customer_id=cust_id[0]).first().id
                ).values('drone__id')).values())
    plan = list(Plan.objects.filter(
        customer=Customer.objects.filter(
            customer_id=cust_id[0]).first().id
            ).values(
                'id',
                'plan',
                'pilot_id__first_name',
                'project_id__project_name',
                'plan_date',
                'start_time',
                'end_time',
                'drone__id'))
    schema = serializers.serialize(
        'json',
        DmsSetting.objects.filter(conf_key='additional_features')
        )
    checklist = serializers.serialize('json', DmsSetting.objects.filter(conf_key='checklist'))
    return Response({
        'drone':drone,
        'plan':plan,
        'schema':json.loads(schema),
        'cust_id':cust_id,
        'checklist':json.loads(checklist)
        },status=200)

@api_view(['GET'])
@csrf_exempt
def ProjectList(request):
    """ Test """
    token=''
    try:
        token = sub('Token ', '', request.META.get('HTTP_AUTHTOKEN', None))
        check_token_exists = DroneConfiguraion.objects.filter(token=token).values()
        if check_token_exists.count():
            cust = DroneAllocation.objects.filter(
                drone_id=check_token_exists[0]['drone_id']
                ).values()
            project = Project.objects.filter(
                customer_id=cust[0]['customer_id']
                ).values('id','project_name')
            return Response({
                'status':True,
                'msg':'Connected successfully!',
                'token':token,
                'project':project
                }, status=200)
        else:
            msg = helper.get_customer_by_token(token,'Token not found!')
            logger.info(msg)
            return Response({'status':False,'msg':'Token not found!'}, status=401)
    except Exception as e:
        # cust = DroneAllocation.objects.filter(drone_id=check_token_exists[0]['drone_id']).values()
        msg = helper.get_customer_by_token(token,str(e))
        logger.error(msg)
        return Response({'success': False, 'msg': str(e)}, status=500)

@api_view(['POST'])
@csrf_exempt
def HandshakeValidation(request):
    """ Test """
    token=''
    try:
        token = sub('Token ', '', request.META.get('HTTP_AUTHTOKEN', None))
        data = json.loads(request.body)
        mac_id = data['mac_id']
        fc_id = data['fc_id']
        drone = 0
        check_token_exists = DroneConfiguraion.objects.filter(token=token).values()
        check_ids_exists = DroneConfiguraion.objects.filter(mac_id=mac_id,fc_id=fc_id).values()
        if check_token_exists.count():
            print('data',check_ids_exists)
            drone = check_token_exists[0]['drone_id']
            if check_ids_exists.count():
                templog = LogTemplate.objects.filter(
                    id = check_ids_exists[0]['template_id']
                    ).values()
                host = check_token_exists[0]['host']
                port = check_token_exists[0]['port']
                username = check_token_exists[0]['username']
                password = check_token_exists[0]['password']
                folder_path = check_token_exists[0]['path']
                with open('LogFields', 'w') as f:
                    f.write(templog[0]['log_fields'])
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host, port=port, username=username, password=password)
                sftp = ssh.open_sftp()
                sftp.put('LogFields',folder_path+'LogFields')
                sftp.close()
                DashboardData.objects.filter(drone=drone).update(error_count=0,gc_con_status=True)
                return Response({'status':True,'msg':'Connected successfully!'}, status=200)
            else:
                DashboardData.objects.filter(drone=drone).update(
                    error_count=F('error_count')+1,
                    gc_con_status=False
                    )
                # cust = DroneAllocation.objects.filter(
                #     drone_id=check_token_exists[0]['drone_id']
                #     ).values()
                msg = helper.get_customer_by_token(token,'Incorrect MAC ID / FC ID!')
                logger.info(msg)
                return Response({'status':False,'msg':'Incorrect MAC ID / FC ID!'}, status=404)
        else:
            if check_ids_exists.count():
                drone = check_ids_exists[0]['drone_id']
                DashboardData.objects.filter(drone=drone).update(
                    error_count=F('error_count')+1,
                    gc_con_status=False
                    )
                # cust = DroneAllocation.objects.filter(drone_id=drone).values()
                msg = helper.get_customer_by_token(token,'Incorrect Token!')
                logger.info(msg)
                return Response({'status':False,'msg':'Incorrect Token!'}, status=404)
            else:
                # cust = DroneAllocation.objects.filter(drone_id=drone).values()
                msg = helper.get_customer_by_token(
                    token,
                    'Incorrect Token or MAC ID or FC ID!'
                    )
                logger.info(msg)
                return Response({
                    'status':False,
                    'msg':'Incorrect Token or MAC ID or FC ID!'
                    }, status=404)
    except Exception as e:

        print('ERROR :'+str(e))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        msg = helper.get_customer_by_token(
            token,
            str(e)
            )
        logger.info(msg)
        return Response({'success': False, 'msg': str(e)}, status=500)
@api_view(['POST'])
@csrf_exempt
@authentication_classes([SessionTokenAuthentication])
@permission_classes([CustomPermission])
def getDrone(request):
    """ Test """
    cust_id = request.customer_id
    # print('request.body',request)
    # print('request.data',request.data)
    data = json.loads(request.body)
    # print('Data',data)
    dd = ''
    drone = list(Drone.objects.filter(
        id__in=DroneAllocation.objects.filter(
            customer=Customer.objects.filter(
                customer_id=cust_id[0]).first().id
                ).values('drone__id'),id=data).values())
    plan = list(Plan.objects.filter(
        customer_id=Customer.objects.filter(
            customer_id=cust_id[0]).first().id,drone=data
            ).values(
                'id',
                'plan',
                'pilot_id__first_name',
                'project_id__project_name',
                'plan_date',
                'start_time',
                'end_time',
                'drone__id'
                ).order_by('id'))
    # print('drone',drone[0]['id'])
    # schema = serializers.serialize('json', DmsSetting.objects.filter(
    #     conf_key='additional_features'
    #     ))

    schema = serializers.serialize('json', DroneType.objects.filter(
        id=drone[0]['drone_type_id']
        ))
    plan_data = list(PlanLog.objects.filter(
            plan_id__customer_id=Customer.objects.filter(
                customer_id=cust_id[0]
                ).first().id,plan_id__drone=data
                ).select_related('Plan').order_by('plan_id').values(p_id=F('plan_id__id'),p_name=F('plan_id__plan')).distinct('plan_id'))

    # plan_data = list(Plan.objects.filter(
    #     customer_id=Customer.objects.filter(
    #         customer_id=cust_id[0]).first().id,drone=data
    #         ).order_by('id').values('id','plan'))

    project_data = list(Plan.objects.filter(
        customer_id=Customer.objects.filter(
            customer_id=cust_id[0]).first().id,
            drone=data
            ).select_related('Project').order_by('project_id').values(p_id=F('project_id__id'),p_name=F('project_id__project_name')).distinct('project_id'))

    # project_data = list(Project.objects.filter(
    #     customer_id=Customer.objects.filter(
    #         customer_id=cust_id[0]).first().id
    #         ).order_by('id').values('id','project_name'))
    customer = Drone.objects.filter(
        id__in=DroneAllocation.objects.filter(
            customer=Customer.objects.filter(
                customer_id=cust_id[0]).first().id
                ).values('drone__id'),id=data).values('image')
    if customer[0]['image']:
        dd =''
        path = (ROOT_DIR+'/attachments/'+customer[0]['image'])
        check_path = Path(path)
        if check_path.is_file():
            with open(path, 'rb') as f:
                dd = (base64.b64encode(f.read()))
    try:
        logs = list(PlanReport.objects.filter(
            log__plan__drone=data,
            log__plan__customer = Customer.objects.filter(
                customer_id=cust_id[0]).first().id )[:10].values(
                    'battery_consumed_max',
                    'distance_to_gcs_max',
                    'flight_distance_max',
                    'flight_time_max',
                    'air_speed',
                    'flight_time',
                    'altitude_relative',
                    'log__plan__plan',
                    'log__plan__project__project_name',
                    'log__plan__plan_date',
                    'log__plan__start_time',
                    'log__plan__end_time'
                    ))
    except:
        logs=''
    checklist = serializers.serialize('json', DmsSetting.objects.filter(conf_key='checklist'))
    return Response({
        'dd':dd,
        'drone':drone,
        'plan':plan,
        'schema':json.loads(schema),
        'cust_id':cust_id,
        'checklist':json.loads(checklist),
        'logs':logs,
        'project_data':project_data,
        'plan_data':plan_data
        },status=200)
@api_view(['POST'])
@csrf_exempt
@authentication_classes([SessionTokenAuthentication])
@permission_classes([CustomPermission])
def getDroneLog(request):
    """ Test """
    cust_id = request.customer_id
    data = json.loads(request.body)
    try:
        logs = list(PlanReport.objects.filter(
            log__plan__drone=data['drone_id'],
            log__plan__customer = Customer.objects.filter(
                customer_id=cust_id[0]).first().id)[:10].values(
                    'battery_consumed_max',
                    'distance_to_gcs_max',
                    'flight_distance_max',
                    'flight_time_max',
                    'air_speed',
                    'flight_time',
                    'altitude_relative',
                    'log__plan__plan',
                    'log__plan__project__project_name',
                    'log__plan__plan_date',
                    'log__plan__start_time',
                    'log__plan__end_time'
                    ).order_by('-id'))
    except Exception as e:
        _cust = DroneAllocation.objects.filter(drone_id=data['drone_id']).values()
        cust = Customer.objects.filter(id=_cust[0]['customer_id']).values()
        msg = cust[0]['account_name']+' - '+str(e)
        logger.error(msg)
        logs=''
    return Response({'logs':logs},status=200)
# @api_view(['POST'])
# @csrf_exempt
# @authentication_classes([SessionTokenAuthentication])
# @permission_classes([CustomPermission])
# def getFilteredReports(request):
#     """ Test """
#     data = json.loads(request.body)
#     cust_id = request.customer_id
#     try:
#         report_data = PlanReport.objects.filter(
#             log__plan__customer = Customer.objects.filter(
#                 customer_id=cust_id[0]).first().id).order_by('-id')
#         if data['filter_from_dt'] !='':
#             report_data = report_data.filter(Q(log__plan__plan_date__gte=data['filter_from_dt']))
#         if data['filter_to_dt'] !='':
#             report_data = report_data.filter(Q(log__plan__plan_date__lte=data['filter_to_dt']))
#         if data['filter_project']!=0:
#             report_data = report_data.filter(log__plan__project__id=data['filter_project'])
#         if data['filter_plan']!=0:
#             report_data = report_data.filter(log__plan__id=data['filter_plan'])
#         if data['filter_limit']>0:
#             report_data = list(report_data.filter(
#                 log__plan__drone=data['drone_id']).values(
#                     'battery_consumed_max',
#                     'distance_to_gcs_max',
#                     'flight_distance_max',
#                     'flight_time_max',
#                     'air_speed',
#                     'flight_time',
#                     'altitude_relative',
#                     'log__plan__plan',
#                     'log__plan__project__project_name',
#                     'log__plan__plan_date'
#                     ))
#         else:
#             report_data = list(report_data.filter(
#                 log__plan__drone=data['drone_id'])[-0:] .values(
#                     'battery_consumed_max',
#                     'distance_to_gcs_max',
#                     'flight_distance_max',
#                     'flight_time_max',
#                     'air_speed',
#                     'flight_time',
#                     'altitude_relative',
#                     'log__plan__plan',
#                     'log__plan__project__project_name',
#                     'log__plan__plan_date'
#                     ))
#         return Response({'report_data':(report_data)},status=200)
#     except Exception as e:
#         _cust = DroneAllocation.objects.filter(drone_id=data['drone_id']).values()
#         cust = Customer.objects.filter(id=_cust[0]['customer_id']).values()
#         msg = cust[0]['account_name']+' - '+str(e)
#         logger.error(msg)
#         report_data =''
#         return Response({'report_data':(report_data),'msg':msg},status=500)

@api_view(['POST'])
@csrf_exempt
@authentication_classes([SessionTokenAuthentication])
@permission_classes([CustomPermission])
def getFilteredReports(request):
    """ Test """

    data = (request.data)
    per_page = (request.query_params.get('offset'))
    cust_id = request.customer_id
    paginator = PageNumberPagination()
    paginator.page_size = int(per_page)
    person_objects = PlanReport.objects.filter(
            log__plan__customer = Customer.objects.filter(
                customer_id=cust_id[0]).first().id).order_by('-id')

    if(type(data['filter_project'])==str):
        data['filter_project'] = 0
    if(type(data['filter_plan'])==str):
        data['filter_plan'] = 0
    try:
        if(data['drone_id'] !=''):
            person_objects = person_objects.filter(log__plan__plan__icontains=data['filter_rpt']) | person_objects.filter(log__plan__project__project_name__icontains=data['filter_rpt']) | person_objects.filter(log__plan__plan_date__icontains=data['filter_rpt']) | person_objects.filter(log__plan__start_time__icontains=data['filter_rpt']) | person_objects.filter(log__plan__end_time__icontains=data['filter_rpt']) | person_objects.filter(flight_distance_max__icontains=data['filter_rpt']) | person_objects.filter(flight_time_max__icontains=data['filter_rpt'])

        if data['filter_project']!=0:
            person_objects = person_objects.filter(log__plan__project__id=data['filter_project'])
        if data['filter_plan']!=0:
            person_objects = person_objects.filter(log__plan__id=data['filter_plan'])
        if (data['filter_from_dt'] != ''):
            date_from = datetime.datetime.strptime(str(data['filter_from_dt']), '%Y-%m-%d')
            person_objects = person_objects.filter(log__plan__plan_date__gte=date_from)
        if (data['filter_to_dt'] != ''):
            date_to = datetime.datetime.strptime(str(data['filter_to_dt']), '%Y-%m-%d')
            person_objects = person_objects.filter(log__plan__plan_date__lte=date_to)
        if (data['time_from'] != ''):
            time_from = datetime.datetime.strptime(str(data['time_from']), '%H:%M:%S')
            person_objects = person_objects.filter(log__plan__start_time__gte=time_from)
        if (data['time_to'] != ''):
            time_to = datetime.datetime.strptime(str(data['time_to']), '%H:%M:%S')
        result_page = paginator.paginate_queryset(person_objects, request)
        serializer = PlanReportSerializer(result_page, many=True)  # MAIN CHANGE IS HERE
        return paginator.get_paginated_response(serializer.data)
    except Exception as e:
        _cust = DroneAllocation.objects.filter(drone_id=data['drone_id']).values()
        cust = Customer.objects.filter(id=_cust[0]['customer_id']).values()
        msg = cust[0]['account_name']+' - '+str(e)
        logger.error(msg)
        report_data =''
        return Response({'report_data':(report_data),'msg':msg},status=500)



@api_view(['GET'])
@authentication_classes([SessionTokenAuthentication])
@permission_classes([CustomPermission])
def GetDroneDetails(request):
    """ Test """
    cust_id = request.customer_id
    drone = list(Drone.objects.filter(id__in=DroneAllocation.objects.filter(
        customer=Customer.objects.filter(
            customer_id=cust_id[0]).first().id
            ).values('drone__id')).values())
    plan = list(Plan.objects.filter(
        customer=Customer.objects.filter(
            customer_id=cust_id[0]).first().id
            ).values(
                'id',
                'plan',
                'pilot_id__first_name',
                'project_id__project_name',
                'plan_date',
                'start_time',
                'end_time',
                'drone__id'
                ))
    schema = serializers.serialize(
        'json',
        DmsSetting.objects.filter(conf_key='additional_features')
        )
    checklist = serializers.serialize(
        'json',
        DmsSetting.objects.filter(conf_key='checklist')
        )
    return Response({
        'drone':drone,
        'plan':plan,
        'schema':json.loads(schema),
        'cust_id':cust_id,
        'checklist':json.loads(checklist)
        },status=200)

@api_view(['POST'])
@csrf_exempt
@authentication_classes([SessionTokenAuthentication])
@permission_classes([CustomPermission])
def getChecklist(request):
    """ Test """
    data = json.loads(request.body)
    id = data['id']
    rules = {}
    maintanence = {}
    approvals = {}
    try:
        rules = Checklist.objects.filter(plan = id,type='Rules').values('schema')
        maintanence = Checklist.objects.filter(plan = id,type='Maintanence').values('schema')
        approvals = Checklist.objects.filter(plan = id,type='Approvals').values('schema')
    except:
        pass
    return Response({'rules':rules,'maintanence':maintanence,'approvals':approvals},status=200)

@api_view(['POST'])
@csrf_exempt
@authentication_classes([SessionTokenAuthentication])
@permission_classes([CustomPermission])
def saveChecklist(request):
    """ Test """
    plan_id = ''
    # print('request.body',((request.body).decode()))
    # return Response({'status':True,'msg':'fsfsdfdf'}, status=200)
    try:
        
        # data = json.loads(request.body)
        data = (request.data)

        # print('request.user',request.user)
        plan_id = data['plan_id']
        rule_data = data['rule_data'][0]
        maintenance_data = data['maintenance_data'][0]
        approval_data = data['approval_data'][0]
        checklist_exists = Checklist.objects.filter(plan = plan_id).count()
        if checklist_exists:
            Checklist.objects.filter(plan = plan_id).delete()
        plan_id = Plan.objects.get(id = data['plan_id'])
        checklist_rule = Checklist(
            plan=plan_id,
            schema = json.dumps(rule_data),
            type = 'Rules',
            user = request.user
        )
        checklist_rule.save()
        checklist_maintenance = Checklist(
            plan=plan_id,
            schema = json.dumps(maintenance_data),
            type = 'Maintanence',
            user = request.user
        )
        checklist_maintenance.save()
        checklist_approval = Checklist(
            plan=plan_id,
            schema = json.dumps(approval_data),
            type = 'Approvals',
            user = request.user
        )
        checklist_approval.save()
        return Response({
            'status':True,
            'msg':'Checklist saved successfully!',
            'data':data
            }, status=200)
    except Exception as e:
        # data = (request.data)
        # print('data',data['rule_data'])
        id = Plan.objects.filter(id=Checklist.objects.filter(plan_id=plan_id).first().customer_id)
        cust = Customer.objects.filter(id=id).values()
        logger.error(cust[0]['account_name']+' - '+str(e))
        return Response({'status':False,'msg':str(e)}, status=500)

@api_view(['POST'])
@csrf_exempt
def saveLogData(request):
    """ Test """
    print('FILE',request.FILES)
    token = ''
    try:
        token = sub('Token ', '', request.META.get('HTTP_AUTHTOKEN', None))
        # print()
        try:
            mac_id = re.search('M(.+?)F', token).group(1)
            fc_id = re.search('F(.+?)T', token).group(1)
            token = re.search('T(.+?)$', token).group(1)
        except AttributeError:
            mac_id = ''
            fc_id = ''
            token = ''
        
        check_token_exists = DroneConfiguraion.objects.filter(
            token=token,
            mac_id=mac_id,
            fc_id=fc_id
            ).values()
        print('check_token_exists.count()',check_token_exists)
        if check_token_exists.count():
            da = DroneAllocation.objects.filter(
                drone_id=check_token_exists[0]['drone_id']
                ).values()
            print('dadadadadadada',da)
            customer_id = Customer.objects.get(id=da[0]['customer_id'])
            c_id = Customer.objects.filter(id=da[0]['customer_id']).values('id')
            data = (request.data)
            plan = data['plan']
            try:
                print('File Read')
                file = (request.FILES.get('file'))
                print('filefilefilefilefilefile',file)
            except Exception as e:
                print('File error')
                # cust = DroneAllocation.objects.filter(
                #     drone_id=check_token_exists[0]['drone_id']
                #     ).values()
                # msg = helper.get_customer_by_token(cust[0]['customer_id'],str(e))
                msg = helper.get_customer_by_token(token,str(e))
                logger.error(msg)
                file = ''
           
            data = pandas.read_csv(file, header=0)
            # print('Pandas Data',data)
            df = pandas.DataFrame(data)
            dd= df.drop_duplicates(subset='flightTime', keep="first")
            plan_id = Plan.objects.get(plan=plan)
            # print('token','re.search token).group(1)')
            try:
                log = PlanLog(
                    plan=plan_id,
                    log_file = file,
                )
                log.save()
            except Exception as e:
                # cust = DroneAllocation.objects.filter(
                #     drone_id=check_token_exists[0]['drone_id']
                #     ).values()
                # msg = helper.get_customer_by_token(cust[0]['customer_id'],str(e))
                msg = helper.get_customer_by_token(token,str(e))
                logger.error(msg)
            battery_consumed = data['battery0.mahConsumed'].max()
            distance_to_gcs = (data['distanceToGCS'].replace('--.--', 0)).max()
            flight_distance = data['flightDistance'].max()
            flight_time = data['flightTime'].max()
            t = time.strptime(flight_time.split(',')[0],'%H:%M:%S')
            new_t= datetime.timedelta(
                    hours=t.tm_hour,
                    minutes=t.tm_min,
                    seconds=t.tm_sec
                    ).total_seconds()
            h = ""
            m = ""
            s = ""
            if new_t>3600:
                h = str(int(new_t/3600))+'h '
            if new_t>60:
                m = str(int((new_t/60)%60))+'m '
            t_max = h+m+str(int(new_t%60))+'s'

            r_flight_time = (list(dd['flightTime']))

            flight_list = []
            for index,a in enumerate(r_flight_time):
                r_flight_time = time.strptime(a.split(',')[0],'%H:%M:%S')
                xx= datetime.timedelta(
                    hours=r_flight_time.tm_hour,
                    minutes=r_flight_time.tm_min,
                    seconds=r_flight_time.tm_sec
                    ).total_seconds()
                hr = ''
                mn = ''
                ss = ''
                if xx>3600:
                    hr = str(int(xx/3600))+'h '
                if xx>60:
                    mn = str(int((xx/60)%60))+'m '
                r_time = hr+mn+str(int(xx%60))+'s'
                flight_list.append(r_time)
            air_speed = list(dd['airSpeed'])
            altitude_relative = list(dd['altitudeRelative'])
            p_id = PlanLog.objects.latest('id')
            log_id = PlanLog.objects.get(id=p_id.id)
            log = PlanReport(
                log=log_id,
                air_speed = air_speed,
                flight_time=json.dumps(flight_list),
                altitude_relative=altitude_relative,
                battery_consumed_max = battery_consumed,
                distance_to_gcs_max = distance_to_gcs,
                flight_distance_max = flight_distance,
                flight_time_max = t_max
            )
            log.save()
            
            planData = Plan.objects.filter(plan=plan).values('drone')
            drone_id = planData[0]['drone']
            drone = Drone.objects.get(id=drone_id)
            dashboard_data = DashboardData.objects.filter(
                drone = drone_id,
                customer_id=c_id[0]['id']
                ).values(
                    'distance',
                    'flying_time',
                    'plans',
                    'id'
                    )
            plans = Plan.objects.filter(drone=drone_id,customer=c_id[0]['id'])
            distance_data = 0
            flying_time_data = 0
            if(dashboard_data[0]['distance']==None or dashboard_data[0]['distance'] == ''):
                distance_data = 0
            else:
                distance_data = dashboard_data[0]['distance']
            if(dashboard_data[0]['flying_time']==None or dashboard_data[0]['flying_time'] == ''):
                flying_time_data = 0
            else:
                flying_time_data = dashboard_data[0]['flying_time']
            
            if dashboard_data.count() > 0:
                distance = float(distance_data)*1000+flight_distance
                flying_time = float(flying_time_data)+new_t
                dData = DashboardData.objects.get(id = dashboard_data[0]['id'])
                dData.distance = round(distance/1000,2)
                dData.flying_time = flying_time
                dData.plans = plans.count()
                dData.save()
            else:
                dData = DashboardData(
                    distance = round(flight_distance/1000,2),
                    flying_time = new_t,
                    plans = plans.count(),
                    gc_con_status = False,
                    status = False,
                    drone = drone,
                    customer_id = customer_id
                )
                dData.save()
            return Response({'status':True,'msg':'Log data saved successfully!'}, status=200)
        else:
            # cust = DroneAllocation.objects.filter(
            #     drone_id=check_token_exists[0]['drone_id']
            #     ).values()
            msg = helper.get_customer_by_token(token,'Invalid Token or MAC ID or FC ID!')
            logger.error(msg)
            return Response({'status':False,'msg':'Invalid Token or MAC ID or FC ID!'}, status=404)
    except Exception as e:
        # token_exists = DroneConfiguraion.objects.filter(token=token).values()
        # cust = DroneAllocation.objects.filter(drone_id=token_exists[0]['drone_id']).values()
        msg = helper.get_customer_by_token(token,str(e))
        logger.error(msg)
        return Response({'success': False, 'msg': str(e)}, status=500)
@api_view(['POST'])
@csrf_exempt
@authentication_classes([SessionTokenAuthentication])
@permission_classes([CustomPermission])
def downloadLog(request):
    """ Test """
    _data = json.loads(request.body)
    log_id = _data['log_id']
    logData = PlanLog.objects.filter(id=log_id).values('log_file','plan__plan','plan__plan_date')
    file_name_new = logData[0]['plan__plan']+'-'+str(logData[0]['plan__plan_date'])
    file_name = (logData[0]['log_file'])
    slipt_file = file_name.split('/')
    path = (ROOT_DIR+'/attachments/'+logData[0]['log_file'])
    with open(path, 'rb') as report:
        data=report.read()
    return Response({'data':data,'filename':file_name_new+'.csv'})

@api_view(['GET'])
@authentication_classes([SessionTokenAuthentication])
@permission_classes([CustomPermission])
def getDashboardData(request):
    """ Test """
    cust_id = request.customer_id
    data = []
    cursor = connection.cursor()
    cursor.execute(
        "select dd.distance,"+
        "dd.flying_time,"+
        "dd.plans,"+
        "dd.gc_con_status,"+
        "dd.error_count,"+
        "dd.status,"+
        "d.model,"+
        "d.id "+
        "from dms_dashboard_datas dd right join dms_drones d on d.id = dd.drone_id  "+
        "inner join dms_customers c on c.id = dd.customer_id "+
        "inner join dms_drone_allocation da on da.drone_id = d.id and da.customer_id = c.id  "+
        "where c.customer_id =  '"+cust_id[0]+"'")
    row = dictfetchall(cursor)
    for r in row:
        if(r['flying_time'] != None and r['flying_time'] !=''):
            seconds = int(float(r['flying_time']))
            h=(seconds//3600)
            m=((seconds%3600)//60)
            s=((seconds%3600)%60)
            t="{}:{}:{}".format(str(h).rjust(2, '0'), str(m).rjust(2, '0'), str(s).rjust(2, '0'))
            r['flying_time'] = t
        if(r['flying_time'] == None or r['flying_time'] ==''):
            r['flying_time'] = 0
        if(r['distance'] == None or r['distance'] ==''):
            r['distance'] =0
        if(r['gc_con_status'] == None or r['gc_con_status'] ==''):
            r['gc_con_status'] = False
        if(r['status'] == None or r['status'] ==''):
            r['status'] = False
        if(r['plans'] == None or r['plans'] ==''):
            r['plans'] = 0
        if(r['model'] == None or r['model'] ==''):
            r['model'] = ''
    N = DmsSetting.objects.filter(conf_key='normal').values('conf_value')
    M = DmsSetting.objects.filter(conf_key='medium').values('conf_value')
    return Response({'data':row,'N':N,'M':M})

def dictfetchall(cursor):
    """ Test """
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

@api_view(['POST'])
@csrf_exempt
def forgotPassword(request):
    """ Test """
    try:
        data = json.loads(request.body)
        email = data['email']
        email_exist = CustomerUser.objects.filter(email=email).values()
        if email_exist.count()<=0:
            msg = helper.get_customer_by_token('','Email does not exist!')
            logger.info(msg)
            return Response({'msg':'Email does not exist!','st':False})
        encryptData = encry.encrypt(str(email))
        encryptData = encryptData.replace("/", "$$$")
        t  = datetime.datetime.now()
        encrypt_t = encry.encrypt(str(t))
        encrypt_t = encrypt_t.replace("/", "$$$")
        subject = "Password Reset"
        end_url = f"{BASE_URL}/masters/reset_password/"+encryptData+"/"+encrypt_t+"/"
        html_message = loader.render_to_string(
            'etl/email/forgot_password.html',
            {
                'app_name': APP_NAME,
                'name': email_exist[0]['first_name'],
                'email':email,
                'end_url':end_url,
                'EMAIL_EXPIRED_AFTER_HOUR':EMAIL_EXPIRED_AFTER_HOUR,
                'BASE_URL':BASE_URL
                })
        send_mail(subject, '', APP_NAME + ' <do_not_reply@domain.com>', [
        email], fail_silently=False, html_message=html_message)
        return Response({
            'msg':'Password reset link has been sent to your email!',
            'st':True,
            'encryptData':encryptData,
            'ddd':end_url
            },status=200)
    except Exception as e:
        # cust = Customer.objects.filter(customer_id=email_exist[0]['customer_id']).values()
        msg = helper.get_customer_by_token('',str(e))
        logger.error(msg)
        return Response({'msg':str(e),'st':False},status=500)

@api_view(['POST'])
@csrf_exempt
@authentication_classes([SessionTokenAuthentication])
@permission_classes([CustomPermission])
def fileUpload(request):
    """ Test """
    _data = request.data
    id = _data['id']
    file = (request.FILES.get('file'))
    customer = CustomerUser.objects.get(id = id)
    customer.profile_image = file
    customer.save()
    path = (ROOT_DIR+'/attachments/Profile_images/'+file.name)
    with open(path, 'rb') as f:
        data = (base64.b64encode(f.read()))
    return Response({'data':data,'filename':file.name})

@api_view(['POST'])
@csrf_exempt
@authentication_classes([SessionTokenAuthentication])
@permission_classes([CustomPermission])
def downloadLicence(request):
    """ Test """
    _data = json.loads(request.body)
    id = _data['id']
    licenceData = CustomerUser.objects.filter(id=id).values('id','pilot_license_file','first_name')
    file_name = licenceData[0]['first_name']+'_licence.pdf'
    slipt_file = file_name.split('/')
    path = (ROOT_DIR+'/attachments/'+licenceData[0]['pilot_license_file'])
    print(path)
    with open(path, 'rb') as report:
        data = (base64.b64encode(report.read()))
    return Response({'data':data,'file_name':file_name})

@api_view(['POST'])
@csrf_exempt
@authentication_classes([SessionTokenAuthentication])
@permission_classes([CustomPermission])
def changePassword(request):
    """ Test """
    try:
        data = json.loads(request.body)
        new_password = data['new_password'].strip()
        old_password = data['password'].strip()
        cust_id = data['id']
        c_id = CustomerUser.objects.filter(id=cust_id).values()
        cust = Customer.objects.filter(id=c_id[0]['customer_id']).values()
        user = User.objects.get(id = c_id[0]['user_id'])
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response({'success': True, 'msg': 'Password changed successfully'}, status=200)
        else:
            logger.info(cust[0]['account_name']+' - '+'Old password doesnt match!')
            return Response({
                'success': False,
                'msg': 'Old password doesnt match!'
                }, status=200)
    except Exception as e:
        msg = helper.get_customer_by_token(c_id[0]['customer_id'],str(e))
        logger.error(msg)
        return Response({
            'success': False,
            'msg': str(e),'c_id':c_id[0]['id']
            }, status=500)

@api_view(['POST'])
@csrf_exempt
@authentication_classes([SessionTokenAuthentication])
@permission_classes([CustomPermission])
def getDroneImage(request):
    """ Test """
    data = request.data
    id = data['id']
    dd = ''
    dd1=''
    customer = Drone.objects.filter(id = id).values('image1','image2')
    if customer[0]['image1']:
        path = (ROOT_DIR+'/attachments/'+customer[0]['image1'])
        check_path = Path(path)
        if check_path.is_file():
            with open(path, 'rb') as f:
                dd = (base64.b64encode(f.read()))
    if customer[0]['image2']:
        path1 = (ROOT_DIR+'/attachments/'+customer[0]['image2'])
        check_path1 = Path(path1)
        if check_path1.is_file():
            with open(path1, 'rb') as ff:
                dd1 = (base64.b64encode(ff.read()))
    return Response({'data':dd,'data1':dd1,'filename':'drone.jpg'})

# @api_view(['POST'])
# @csrf_exempt
# def getLoginToken(request):
#     """ Test """
#     data = request.data
#     token = ''
#     token = data['token']
#     tm = token.replace("@*@", "/")
#     encryptData = tm.replace("$*$", "+")
#     token = encry.decrypt(encryptData)
#     token_obj = Token.objects.get(key=token)
#     user = token_obj.user
#     request.user = user
#     request.email = user.email
#     if not user.is_superuser:
#         request.role = UserRoleModel.objects.filter(
#             user_id=user
#             ).values_list('role_id__name', flat=True)[0]
#         request.permissions = GroupPermissionModel.objects.filter(
#             group_id=RoleGroupModel.objects.filter(
#                 role_id=UserRoleModel.objects.filter(
#                     user_id=user
#                     ).first().role_id
#                     ).first().group_id
#                     ).values_list('permission_id__code', flat=True)
#         request.customer_id = Customer.objects.filter(
#             id=CustomerUser.objects.filter(
#                 email = user.email
#                 ).first().customer_id
#                 ).values_list('customer_id', flat=True)
#     role_perm = {
#         'id': request.user.id,
#         'username': request.user.username,
#         'role': request.role,
#         'email' : request.email,
#         'name' : request.user.first_name,
#         'last_name' : request.user.last_name,
#         'permissions': request.permissions,
#         'customer_id': request.customer_id,
#         'is_superuser': request.user.is_superuser
#     }
#     return Response({'token':token,'role_perm':role_perm})

@api_view(['POST'])
@csrf_exempt
@authentication_classes([SessionTokenAuthentication])
@permission_classes([CustomPermission])
def getProfileSchema(request):
    """ Test """
    profile_schema = DmsSetting.objects.filter(conf_key='profile_schema').values('conf_value')
    return Response(profile_schema)

@api_view(['POST'])
@csrf_exempt
@authentication_classes([SessionTokenAuthentication])
@permission_classes([CustomPermission])
def getPlan(request):
    """ Test """
    cust_id = request.customer_id
    data = json.loads(request.body)
    # list(PlanLog.objects.select_related('Plan').values())
    if data['project_id'] == '0':
        plan_data = list(PlanLog.objects.filter(
            plan_id__customer_id=Customer.objects.filter(
                customer_id=cust_id[0]
                ).first().id,plan_id__drone_id=data['drone']
                ).select_related('Plan').order_by('plan_id').values(p_id=F('plan_id__id'),p_name=F('plan_id__plan')).distinct('plan_id'))
    else:

        plan_data = list(PlanLog.objects.filter(
            plan_id__customer_id=Customer.objects.filter(
                customer_id=cust_id[0]
                ).first().id,plan_id__drone_id=data['drone'],
                plan_id__project_id = data['project_id']
                ).select_related('Plan').order_by('plan_id').values(p_id=F('plan_id__id'),p_name=F('plan_id__plan')).distinct('plan_id'))
                
        # plan_data = list(Plan.objects.filter(
        #     customer_id=Customer.objects.filter(
        #         customer_id=cust_id[0]
        #         ).first().id,drone_id=data['drone'],
        #         project_id = data['project_id']
        #         ).order_by('id').values('id','plan'))
    return Response({'plan_data':plan_data})

@api_view(['GET'])
@authentication_classes([SessionTokenAuthentication])
@permission_classes([CustomPermission])
def GetReleasePlan(request):
    """ Test """
    releasedate = DmsSetting.objects.filter(conf_key='releasedate').values('conf_value')
    version = DmsSetting.objects.filter(conf_key='version').values('conf_value')
    releasedays = DmsSetting.objects.filter(conf_key='releasedays').values('conf_value')
    return Response({'RELEASE_DATE':releasedate,'VERSION':version, 'RELEASE_DAYS':releasedays})

@api_view(['GET'])
@csrf_exempt
def PilotList(request):
    """ Test """
    token=''
    try:
        token = sub('Token ', '', request.META.get('HTTP_AUTHTOKEN', None))
        check_token_exists = DroneConfiguraion.objects.filter(token=token).values()
        if check_token_exists.count():
            cust = DroneAllocation.objects.filter(
                drone_id=check_token_exists[0]['drone_id']
                ).values()
            pilot = CustomerUser.objects.filter(
                customer_id=cust[0]['customer_id'],
                pilot=True
                ).values('id','first_name','last_name')
            print('pilot',pilot)
            return Response({
                'status':True,
                'msg':'Connected successfully!',
                'token':token,
                'pilot':pilot
                }, status=200)
        else:
            msg = helper.get_customer_by_token(token,'Token not found!')
            logger.info(msg)
            return Response({'status':False,'msg':'Token not found!'}, status=404)
    except Exception as e:
        msg = helper.get_customer_by_token(token,str(e))
        logger.error(msg)
        return Response({'success': False, 'msg': str(e)}, status=500)

@api_view(['GET'])
@csrf_exempt
def UpdateSubsetFields(request):
    """ Test """
    token=''
    try:
        token = sub('Token ', '', request.META.get('HTTP_AUTHTOKEN', None))
        check_token_exists = DroneConfiguraion.objects.filter(token=token).values()
        if check_token_exists.count():
            log_fields = LogTemplate.objects.filter(
                id = check_token_exists[0]['template_id']
                ).values()
            return Response({
                'status':True,
                'msg':'Connected successfully!',
                'token':token,
                'log_fields':log_fields[0]['log_fields']
                }, status=200)
        else:
            msg = helper.get_customer_by_token(token,'Token not found!')
            logger.info(msg)
            return Response({'status':False,'msg':'Token not found!'}, status=404)
    except Exception as e:
        msg = helper.get_customer_by_token(token,str(e))
        logger.error(msg)
        return Response({'success': False, 'msg': str(e)}, status=500)

@api_view(['POST'])
@csrf_exempt
def SaveConsumptionLog(request):
    """ Test """
    token = ''
    try:
        data = json.loads(request.body)
        # sdfsdf
        cpu_usage = data['cpu_usage']
        virtual_memory  = data['virtual_memory']
        swap_memory = data['swap_memory']
        timestamp = data['timestamp']
        token = sub('Token ', '', request.META.get('HTTP_AUTHTOKEN', None))
        try:
            mac_id = re.search('M(.+?)F', token).group(1)
            fc_id = re.search('F(.+?)T', token).group(1)
            token = re.search('T(.+?)$', token).group(1)
        except AttributeError:
            mac_id = ''
            fc_id = ''
            token = ''
        check_token_exists = DroneConfiguraion.objects.filter(
            token=token,
            mac_id=mac_id,
            fc_id=fc_id
            ).values()
        if check_token_exists.count():
            drone = Drone.objects.get(id=check_token_exists[0]['drone_id'])
            cLog = ConsumptionLog(
                    drone = drone,
                    cpu_usage = cpu_usage,
                    virtual_memory  = virtual_memory ,
                    swap_memory = swap_memory,
                    timestamp = timestamp
                )
            cLog.save()
            return Response({
                'status':True,
                'msg':'Consumption Log saved successfully!'
                }, status=200)
        else:
            # token_exists = DroneConfiguraion.objects.filter(
            #     token=token
            #     ).values()
            # cust = DroneAllocation.objects.filter(
            #     drone_id=token_exists[0]['drone_id']
            #     ).values()
            msg = helper.get_customer_by_token(token,'Invalid Token/MAC ID/FC ID!')
            logger.info(msg)
            return Response({
                'status':False,
                'msg':'Invalid Token/MAC ID/FC ID!'
                }, status=404)

    except Exception as e:
        msg = helper.get_customer_by_token(token,str(e))
        logger.error(msg)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return Response({'success': False, 'msg': str(e)}, status=500)
