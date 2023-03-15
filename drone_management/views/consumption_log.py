from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from userpermissions.decorators import permission_decorator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.views import View
import json
from django.core import serializers
from masters.models import DmsSetting, Company, Country, Designation, State, Product,Category, ProductType, TransactionLog, DroneAllocation, LogTemplate,DroneConfiguraion,ConsumptionLog
from drone_management.models import DroneType, BatteryMaster, RCMaster, SensorMaster, CameraMaster,Drone,DroneComponent, DroneStatus, DronePurpose
import datetime
from drone_management.form import SaveDroneFrom, SaveDroneUpdateFrom, SaveConfigFrom
from django.contrib.auth.models import User
from utils import helper
import os,sys
from ast import literal_eval
from django.db.models import F
from django.conf import settings
from dms.Key_generation import random_key,pgpy_key
import secrets
import paramiko
from utils.encryption import aes
from django.views.decorators.csrf import csrf_exempt
encry = aes(settings.KEY, settings.IV)
# include('drone_management.Key_generator')
# from random_key pgpy_key import Key_generator
TABLE_ROW_LIMIT = settings.TABLE_ROW_LIMIT
ROOT_DIR = os.path.abspath(os.curdir)

class ConsumptionLogList(LoginRequiredMixin, View):
    @method_decorator(permission_decorator(permission='consumption-log-list'))
    def get(self, request):
        query_url = ''
        logs = ConsumptionLog.objects.filter().order_by("-created_on")
        
        try:
            query = request.GET['search']
        except Exception as e:
            query = ''
        if query:
            logdata = ConsumptionLog.objects.filter(
                Q(virtual_memory__icontains=request.GET['search']) |
                Q(cpu_usage__icontains=request.GET["search"]) |
                Q(swap_memory__icontains=request.GET["search"]) |
                Q(status__icontains=request.GET["search"]) |
                Q(drone_id__model__icontains=request.GET["search"])
                # |
                # Q(remote_control__name__icontains=request.GET["search"])
                ).order_by("-created_on")
        else:
            logdata = ConsumptionLog.objects.filter().order_by("-created_on")

        page = request.GET.get('page', 1)
        paginator = Paginator(logdata, TABLE_ROW_LIMIT)

        try:
            logs = paginator.page(page)
        except PageNotAnInteger:
            logs = paginator.page(1)
        except EmptyPage:
            logs = paginator.page(paginator.num_pages)
        if query:
            query_url = '&search='+query
        return render(request, 'consumption_log/list.html', {'data': logdata, 'logs': logs, 'query': query, 'query_url':query_url})
class UpdateLogStatus(LoginRequiredMixin, View):
    @method_decorator(permission_decorator(permission='consumption-log-list'))
    # @csrf_exempt
    def get(self, request):
        try:
            ConsumptionLog.objects.filter(status = 'Unread').update(status='Read')
            return JsonResponse({'success': True, 'msg': 'Statuss updated successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'msg': str(e)}, status=500)