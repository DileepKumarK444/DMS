from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
import json
from masters.models import Project
from masters.models import Customer, CustomerUser
from dms.authentication import SessionTokenAuthentication
from dms.permission import CustomPermission

from utils import helper
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
@csrf_exempt
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
@authentication_classes([SessionTokenAuthentication])
@permission_classes([CustomPermission])
def AddProject(request):
    _cust_id = ''
    try:
        _cust_id = helper.get_customer_id(request)
        # fsdfsf
        data = json.loads(request.body)
        cust_id = request.customer_id
        print('cust_id',cust_id)
        project_name = data['project_name']
        mission_commander = CustomerUser.objects.get(id=int(data['mission_commander']))
        start_date = data['start_date']
        end_date = data['end_date']
        
        
        project_name_check = Project.objects.filter(project_name=project_name,customer_id__customer_id=cust_id[0]).count()
        if project_name_check:
            msg = helper.get_customer_details(_cust_id,'Sorry! Project Name already exist.')
            logger.info(msg)
            return Response({'success': 'exist', 'msg': 'Sorry! Project Name already exist.'})
        try:
            customerid_check = Customer.objects.filter(customer_id=cust_id[0]).count()
        except:
            msg = helper.get_customer_details(_cust_id,'Sorry! You do not have permission to create project!')
            logger.info(msg)
            return Response({'success': 'exist', 'msg': 'Sorry! You do not have permission to create project!'})
        customer_id = Customer.objects.get(customer_id=cust_id[0])
        project = Project(
            project_name=project_name,
            mission_commander = mission_commander,
            start_date = start_date,
            end_date = end_date,
            customer = customer_id
        )
        project.save()

        return Response({'success': 'true', 'msg': 'Project created successfully.'})
    except Exception as e:
        msg = helper.get_customer_details(_cust_id,'Sorry! error on Project save')
        logger.info(msg)
        return Response({'success': 'false', 'msg': 'Sorry! error on Project save'})


@api_view(['GET'])
# @csrf_exempt
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
@authentication_classes([SessionTokenAuthentication])
@permission_classes([CustomPermission])
def GetProjectList(request):
    
    _cust_id = helper.get_customer_id(request)
    cust_id = request.customer_id
    customer_id = Customer.objects.filter(customer_id=cust_id[0]).first().id
    projects = list(Project.objects.filter(customer_id = customer_id).values('id','project_name','mission_commander_id__first_name','start_date','end_date'))
    return Response(projects)
    

@api_view(['POST'])
@csrf_exempt
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
@authentication_classes([SessionTokenAuthentication])
@permission_classes([CustomPermission])
def DeleteProject(request):
    _cust_id = ''
    try:
        _cust_id = helper.get_customer_id(request)
        data = json.loads(request.body)
        cust_id = request.customer_id
        _id = data['id']
        Project.objects.filter(id = _id).delete()

        return Response({'success': 'true', 'msg': 'Project deleted successfully.'})
    except Exception as e:
        msg = helper.get_customer_details(_cust_id,'Sorry! error on Project delete')
        logger.info(msg)
        return Response({'success': 'true', 'msg': 'Sorry! error on Project delete'})

@api_view(['POST'])
@csrf_exempt
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
@authentication_classes([SessionTokenAuthentication])
@permission_classes([CustomPermission])
def getSelectedPojectDetails(request):
    
    data = json.loads(request.body)
    cust_id = request.customer_id
    _id = data['id']
    project = Project.objects.filter(id = _id).values("id","project_name","mission_commander_id__id","start_date","end_date") 
    return Response(project)
    

@api_view(['POST'])
@csrf_exempt
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
@authentication_classes([SessionTokenAuthentication])
@permission_classes([CustomPermission])
def ProjectUpdate(request):
    _cust_id = ''
    try:
        _cust_id = helper.get_customer_id(request)
        data = json.loads(request.body)
        _id = data['id']
        cust_id = request.customer_id
        project_name = data['project_name']

        project_name_check = Project.objects.filter(project_name=project_name,customer_id__customer_id=cust_id[0]).exclude(id=_id).count()
        if project_name_check:
            return Response({'success': 'exist', 'msg': 'Sorry! Project Name already exist.'})

        mission_commander = CustomerUser.objects.get(id=int(data['mission_commander']))
        start_date = data['start_date']
        end_date = data['end_date']
        project = Project.objects.get(id = _id)
        project.project_name = project_name
        project.mission_commander = mission_commander
        project.start_date = start_date
        project.end_date = end_date

        project.save()
        
        return Response({'success': 'true', 'msg': 'Project updated successfully.'})
    except Exception as e:
        msg = helper.get_customer_details(_cust_id,'Sorry! error on Project update')
        logger.info(msg)
        return Response({'success': 'false', 'msg': 'Sorry! error on Project update'})