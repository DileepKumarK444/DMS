from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
import json
from masters.models import Customer, CustomerUser, DashboardData, DroneConfiguraion, DroneAllocation
from masters.models import Project, Plan
from drone_management.models import Drone
from dms.authentication import SessionTokenAuthentication
from dms.permission import CustomPermission
from re import sub
import sys
import os
import datetime
from django.conf import settings
from django.core.files.base import ContentFile

from pathlib import Path
from django.core.files import File

from utils import helper
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
@csrf_exempt
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# @authentication_classes([SessionTokenAuthentication])
# @permission_classes([CustomPermission])
def SavePlan(request):
    token=''
    try:
        js = json.loads(request.body.decode('utf-8'))
        data = json.loads(js['data'])
        file = json.loads(js['file'])
        print("FILE",file)
        print('data ',data['plan'])

        project_name = data['project_name']
        plan_date = data['plan_date']
        start_time = data['start_time']
        end_time = data['end_time']
        first_name = data['first_name']
        last_name = data['last_name']
        plan = data['plan']
        # print('file ',js['file'])

        # data = (request.data)
        # file = (request.FILES.get('plan_file'))
        cust_id = request.customer_id
        token = sub('Token ', '', request.META.get('HTTP_AUTHTOKEN', None))
        check_token_exists = DroneConfiguraion.objects.filter(token=token).values()
        # drone = data['drone_id']
        if check_token_exists.count():

            f = open(os.path.join(settings.MEDIA_ROOT,'plan_files/temp/'+plan+'.plan'), "a")
            f.write(str(file))
            f.close()

            #open and read the file after the appending:
            # f = open(os.path.join(settings.MEDIA_ROOT,'plan_files/'+plan+'.plan'), "r")
            # print(f.read())
            path = Path(os.path.join(settings.MEDIA_ROOT,'plan_files/temp/'+plan+'.plan'))

            print('check_token_exists',check_token_exists)
            da = DroneAllocation.objects.filter(drone_id=check_token_exists[0]['drone_id']).values()
            project = Project.objects.get(project_name=data['project_name'],
                customer_id=da[0]['customer_id'])
            pilot = CustomerUser.objects.get(first_name=data['first_name'],
                last_name=data['last_name'],customer_id=da[0]['customer_id'])
            plan = data['plan']
            plan_date = datetime.datetime.strptime(
                data['plan_date'], '%a %b %d %Y').strftime('%Y-%m-%d'
                )
            start_time = data['start_time']
            end_time = data['end_time']
            try:
                id = data['id']
            except:
                id = ''
            customer_id = Customer.objects.get(id=da[0]['customer_id'])

            c_id = Customer.objects.filter(id=da[0]['customer_id']).values('id')

            drone_id = Drone.objects.get(id=check_token_exists[0]['drone_id'])
            if(id == '' or id == 0):
                plan_name_check = Plan.objects.filter(plan=plan).count()
                if plan_name_check:
                    msg = helper.get_customer_by_token(token,'Sorry! Plan Name already exist.')
                    logger.info(msg)
                    return Response({'success': False, 'msg': 'Sorry! Plan Name already exist.'})
                plan_data = Plan(
                    plan = plan,
                    pilot = pilot,
                    project = project,
                    plan_date = plan_date,
                    start_time = start_time,
                    end_time = end_time,
                    customer = customer_id,
                    drone = drone_id,
                    # plan_file = f
                )
                plan_data.save()
                plan_id = Plan.objects.latest('id')
                p = Plan.objects.get(id=plan_id.id)
                # os.remove(os.path.join(settings.MEDIA_ROOT,'plan_files/'+plan+'.plan'))
                with path.open(mode='rb') as f:
                    p.plan_file = File(f, name=path.name)
                    p.save()
                os.remove(os.path.join(settings.MEDIA_ROOT,'plan_files/temp/'+plan+'.plan'))

                print("c_id[0]['id']",c_id[0]['id'])
                dashboard_data = DashboardData.objects.filter(
                    drone = check_token_exists[0]['drone_id'],
                    customer = c_id[0]['id']).values('distance','flying_time','plans','id')
                print('dashboard_data',dashboard_data)
                plans = Plan.objects.filter(drone=drone_id,customer = c_id[0]['id'])
                if dashboard_data.count() > 0:
                    dData = DashboardData.objects.get(id = dashboard_data[0]['id'])
                    dData.plans = plans.count()
            
                    dData.save()
                else:
                    dData = DashboardData(
                        plans = plans.count(),
                        gc_con_status = False,
                        status = False,
                        drone = drone_id,
                        customer = customer_id
                    )
                    dData.save()
                return Response({'success': True, 'msg': 'Plan Saved successfully.'})
            else:
                plan_name_check = Plan.objects.filter(plan=plan).exclude(id=id).count()
                if plan_name_check:
                    msg = helper.get_customer_by_token(token,'Sorry! Plan Name already exist.')
                    logger.info(msg)
                    return Response({'success': False, 'msg': 'Sorry! Plan Name already exist.'})
                plan_data = Plan.objects.get(id=id)
                plan_data.plan = plan
                plan_data.pilot = pilot
                plan_data.project = project
                plan_data.plan_date = plan_date
                plan_data.start_time = start_time
                plan_data.end_time = end_time
                plan_data.customer = customer_id
                plan_data.drone = drone_id
                plan_data.plan_file = file
                plan_data.save()
                return Response({'success': True, 'msg': 'Plan updated successfully.'})
        else:
            msg = helper.get_customer_by_token(token,'Token not found!')
            logger.info(msg)
            return Response({'status':False,'msg':'Token not found!'}, status=404)
    except Exception as e:
            # return JsonResponse({'success': False, 'msg': str(e)}, status=500)
        print('ERROR :'+str(e))
        msg = helper.get_customer_by_token(token,str(e))
        logger.info(msg)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return Response({'success': False, 'msg': str(e)}, status=500)

@api_view(['POST'])
@csrf_exempt
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# @authentication_classes([SessionTokenAuthentication])
# @permission_classes([CustomPermission])
def UpdatePlan(request):
    token = ''
    try:
        js = json.loads(request.body.decode('utf-8'))
        data = json.loads(js['data'])
        file = json.loads(js['file'])
        project_name = data['project_name']
        plan_date = data['plan_date']
        start_time = data['start_time']
        end_time = data['end_time']
        first_name = data['first_name']
        last_name = data['last_name']
        plan = data['plan']
        cust_id = request.customer_id
        token = sub('Token ', '', request.META.get('HTTP_AUTHTOKEN', None))
        check_token_exists = DroneConfiguraion.objects.filter(token=token).values()
        if check_token_exists.count():
            f = open(os.path.join(settings.MEDIA_ROOT,'plan_files/temp/'+plan+'.plan'), "a")
            f.write(str(file))
            f.close()
            da = DroneAllocation.objects.filter(drone_id=check_token_exists[0]['drone_id']).values()
            project = Project.objects.get(project_name=data['project_name'],customer_id=da[0]['customer_id'])
            pilot = CustomerUser.objects.get(first_name=data['first_name'],last_name=data['last_name'],customer_id=da[0]['customer_id'])
            plan = data['plan']
            plan_date = datetime.datetime.strptime(data['plan_date'], '%a %b %d %Y').strftime('%Y-%m-%d')
            start_time = data['start_time']
            end_time = data['end_time']
            customer_id = Customer.objects.get(id=da[0]['customer_id'])
            c_id = Customer.objects.filter(id=da[0]['customer_id']).values('id')
            drone_id = Drone.objects.get(id=check_token_exists[0]['drone_id'])
            plan_name_check = Plan.objects.filter(plan=plan).exclude(plan=plan).count()
            if plan_name_check:
                msg = helper.get_customer_by_token(token,'Sorry! Plan Name already exist.')
                logger.info(msg)
                return Response({'success': False, 'msg': 'Sorry! Plan Name already exist.'})
            plan_data = Plan.objects.get(plan=plan)
            plan_data.plan = plan
            plan_data.pilot = pilot
            plan_data.project = project
            plan_data.plan_date = plan_date
            plan_data.start_time = start_time
            plan_data.end_time = end_time
            plan_data.customer = customer_id
            plan_data.drone = drone_id
            plan_data.save()
            plan_id = Plan.objects.filter(plan=plan).values()
            p = Plan.objects.get(id=plan_id[0]['id'])
            path = Path(os.path.join(settings.MEDIA_ROOT,'plan_files/temp/'+plan+'.plan'))
            try:
                path1 = Path(os.path.join(settings.MEDIA_ROOT,'plan_files/'+plan+'.plan'))
                if(path1.exists()):
                    os.remove(os.path.join(settings.MEDIA_ROOT,'plan_files/'+plan+'.plan'))
            except:
                pass
            with path.open(mode='rb') as f:
                p.plan_file = File(f, name=path.name)
                p.save()
            os.remove(os.path.join(settings.MEDIA_ROOT,'plan_files/temp/'+plan+'.plan'))
            return Response({'success': True, 'msg': 'Plan Updated successfully.'})
        else:
            msg = helper.get_customer_by_token(token,'Token not found!')
            logger.info(msg)
            return Response({'status':False,'msg':'Token not found!'}, status=404)
    except Exception as e:
        print('ERROR :'+str(e))
        msg = helper.get_customer_by_token(token,str(e))
        logger.info(msg)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return Response({'success': False, 'msg': str(e)}, status=500)

# @api_view(['POST'])
# @csrf_exempt
# @authentication_classes([SessionTokenAuthentication])
# @permission_classes([CustomPermission])
# def RunningPlanData(request):
#     data = json.loads(request.body)
#     flight_time = data['flight_time']
#     altitude = data['altitude']
#     battery_consumed = data['battery_consumed']
#     distance_covered = data['distance_covered']
#     location = data['location']
#     pilot_id = data['pilot_id']
#     project_id = data['project_id']
#     drone_id = data['drone_id']
#     return Response({'success': 'true', 'msg': 'Data send to AVM successsfully.'})
