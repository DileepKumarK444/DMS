# pylint: disable=no-member
"""
Customer Master
"""

import os
# pylint: disable=E0401
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from django.views import View
from django.utils.decorators import method_decorator
from django.conf import settings
from userpermissions.decorators import permission_decorator
from drone_management.models import DronePurpose, DroneType
from masters.models import Drone
from masters.form import SaveDroneTypeForm, UpdateDroneTypeForm
from utils.encryption import aes

encry = aes(settings.KEY, settings.IV)
ROOT_DIR = os.path.abspath(os.curdir)

BASE_URL = settings.BASE_URL
APP_NAME = settings.APP_NAME
DMS_URL = settings.DMS_URL
TABLE_ROW_LIMIT = settings.TABLE_ROW_LIMIT
class DroneTypeList(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Drone Type List"""
    @method_decorator(permission_decorator(permission='drone-type-list'))
    def get(self, request):
        """Drone Type List Get"""
        query_url = ''
        # dronetype = DroneType.objects.filter().order_by('-id')
        try:
            query = request.GET['search']
        except: # pylint: disable=W0702
            query = ''
        if query:
            dronetypedata = DroneType.objects.filter(
                Q(name__icontains=request.GET['search']) |
                Q(purpose__name__icontains=request.GET['search']) |
                Q(description__icontains=request.GET["search"])
                ).order_by('-id')
        else:
            dronetypedata = DroneType.objects.all().order_by('-id')
        page = request.GET.get('page', 1)
        paginator = Paginator(dronetypedata, TABLE_ROW_LIMIT)
        try:
            dronetype = paginator.page(page)
        except PageNotAnInteger:
            dronetype = paginator.page(1)
        except EmptyPage:
            dronetype = paginator.page(paginator.num_pages)
        if query:
            query_url = '&search='+query
        purpose = DronePurpose.objects.all()
        return render(request, 'drone_type/list.html', {'data': dronetypedata, 'query': query, 'dronetype': dronetype,'query_url':query_url,'purpose':purpose,'msg':''})

    @method_decorator(permission_decorator(permission='drone-type-delete'))
    def delete(self, request):
        """Drone Type List Delete"""
        try:
            type_check = Drone.objects.filter(drone_type=request.GET['id']).count()
            if type_check:
                return JsonResponse({'success': 'exist', 'msg': 'Sorry can\'t delete, Drone Type already have transaction.'})
            data = DroneType.objects.get(id=request.GET['id'])
            data.delete()
            return JsonResponse({'success': True, 'url': '/masters/drone_type/'}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=200)
class DroneTypeAdd(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Drone Type Add"""
    @method_decorator(permission_decorator(permission='drone-type-save'))
    def post(self, request):
        """Drone Type Add Post"""
        try:
            form = SaveDroneTypeForm(request.POST)
            if form.is_valid():
                name = request.POST['txt_name']
                description = request.POST['description']
                additional_features = request.POST['features']
                purpose = DronePurpose.objects.get(id=request.POST['purpose'])
                # type_chcek = DroneType.objects.filter(name=name,purpose=request.POST['purpose']).count()
                # if type_chcek:
                #     return JsonResponse({'success': 'exist', 'msg': 'Sorry! Drone Type already exist.'})
                dronetype = DroneType(
                name=name,
                description = description,
                purpose = purpose,
                additional_features = additional_features,
                created_by = request.user
                )
                dronetype.save()
                return JsonResponse({'success': True, 'msg': 'Successfully Added'}, status=200)
            return JsonResponse({'success': False, 'errors': form.errors}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=500)

class DroneTypeUpdate(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Drone Type Update"""
    @method_decorator(permission_decorator(permission='drone-type-update'))
    def post(self, request):
        """Drone Type Update Post"""
        try:
            form = UpdateDroneTypeForm(request.POST)
            if form.is_valid():
                name = request.POST['txt_name']
                description = request.POST['description']
                type_id = request.POST['typeid']
                additional_features = request.POST['features']
                # type_check = DroneType.objects.filter(name=name,purpose=request.POST['purpose']).exclude(id=type_id).count()
                # if type_check:
                #     return JsonResponse({'success': 'exist', 'msg': 'Sorry! Drone Type already exist.'})
                purpose = DronePurpose.objects.get(id=request.POST['purpose'])
                dronetype = DroneType.objects.get(id=type_id)
                dronetype.name = name
                dronetype.description = description
                dronetype.purpose = purpose
                dronetype.additional_features=additional_features
                dronetype.created_by = request.user
                dronetype.save()
                return JsonResponse({'success': True, 'msg': 'Successfully Updated'}, status=200)
            return JsonResponse({'success': False, 'errors': form.errors}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=500)
