# from django.shortcuts import render
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.decorators import authentication_classes
# from rest_framework.decorators import permission_classes
# from rest_framework.permissions import IsAuthenticated
# from django.contrib.auth import authenticate
# import json
# from masters.models import Customer
# from masters.models import Pilot
# from django.core.files.storage import FileSystemStorage
# import os
# from dms.settings import MEDIA_ROOT
# from dms.authentication import SessionTokenAuthentication
# from dms.permission import CustomPermission
# from utils import helper
# import logging

# logger = logging.getLogger(__name__)

# @api_view(['POST'])
# @csrf_exempt
# # @authentication_classes([TokenAuthentication])
# # @permission_classes([IsAuthenticated])
# @authentication_classes([SessionTokenAuthentication])
# @permission_classes([CustomPermission])
# def AddPilot(request):
#     _cust_id = ''
#     try:
#         _cust_id = helper.get_customer_id(request)
#         cust_id = request.customer_id
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         phone = request.POST['phone']
#         email = request.POST['email']
#         pilot_license = request.FILES['pilot_license']
#         expiry_date = request.POST['expiry_date']
#         customer_id = cust_id[0]
#         active = True
#         email_check = Pilot.objects.filter(email=email).count()
#         if email_check:
#             msg = helper.get_customer_details(_cust_id,'Sorry! email ID already exist.')
#             logger.info(msg)
#             return Response({'success': 'exist', 'msg': 'Sorry! email ID already exist.'})
#         try:
#             cust_admin = Customer.objects.get(customer_id=customer_id)
#         except:
#             msg = helper.get_customer_details(_cust_id,'Sorry! Customer admin does not exist.')
#             logger.info(msg)
#             return Response({'success': 'false', 'msg': 'Sorry! Customer admin does not exist.'})
        
#         pilot = Pilot(
#             first_name=first_name,
#             last_name = last_name,
#             email = email,
#             phone = phone,
#             pilot_license = pilot_license,
#             expiry_date = expiry_date,
#             status = active,
#             customer_id = customer_id
#         )
#         pilot.save()

#         return Response({'success': 'true', 'msg': 'Pilot created successfully.'})
#     except Exception as e:
#         msg = helper.get_customer_details(_cust_id,'Sorry! error Pilot creation')
#         logger.info(msg)
#         return Response({'success': 'false', 'msg': 'Sorry! error Pilot creation'})

# @api_view(['GET'])
# # @csrf_exempt
# # @authentication_classes([TokenAuthentication])
# # @permission_classes([IsAuthenticated])
# @authentication_classes([SessionTokenAuthentication])
# @permission_classes([CustomPermission])
# def GetPilotList(request):
#     cust_id = request.customer_id
#     pilot = list(Pilot.objects.filter(customer_id = cust_id[0]).values())
    
#     return Response(pilot)

# def _upload_file(attachment, directory):
#     fs = FileSystemStorage()
#     name = fs.save(MEDIA_ROOT + '/' + directory +
#                    '/' + attachment, attachment)
#     path, filename = os.path.split(name)
#     return filename