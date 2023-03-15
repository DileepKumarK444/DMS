# pylint: disable=no-member
"""
Purpose Master
"""
# pylint: disable=E0401
import os

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from django.views import View
from django.conf import settings

from masters.form import SavePurposeForm,UpdatePurposeForm
from masters.models import Drone
from drone_management.models import DronePurpose


from userpermissions.decorators import permission_decorator

from utils.encryption import aes

encry = aes(settings.KEY, settings.IV)
ROOT_DIR = os.path.abspath(os.curdir)

BASE_URL = settings.BASE_URL
APP_NAME = settings.APP_NAME
DMS_URL = settings.DMS_URL
TABLE_ROW_LIMIT = settings.TABLE_ROW_LIMIT

class PurposeList(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Purpose List"""
    @method_decorator(permission_decorator(permission='purpose-list'))
    def get(self, request):
        """Purpose List Get"""
        query_url = ''
        # purpose = DronePurpose.objects.filter().order_by('-id')
        try:
            query = request.GET['search']
        except: # pylint: disable=W0702
            query = ''
        if query:
            purposedata = DronePurpose.objects.filter(
                Q(name__icontains=request.GET['search']) |
                Q(description__icontains=request.GET["search"])
                ).order_by('-id')
        else:
            purposedata = DronePurpose.objects.all().order_by('-id')
        page = request.GET.get('page', 1)
        paginator = Paginator(purposedata, TABLE_ROW_LIMIT)
        try:
            purpose = paginator.page(page)
        except PageNotAnInteger:
            purpose = paginator.page(1)
        except EmptyPage:
            purpose = paginator.page(paginator.num_pages)
        if query:
            query_url = '&search='+query
        return render(request, 'purpose/list.html', {'data': purposedata, 'query': query, 'purpose': purpose,'query_url':query_url})

    @method_decorator(permission_decorator(permission='purpose-delete'))
    def delete(self, request):
        """Purpose List Delete"""
        try:
            drone_check = Drone.objects.filter(drone_purpose=request.GET['id']).count()
            if drone_check:
                return JsonResponse({'success': 'exist', 'msg': 'Sorry can\'t delete, Drone Purpose already have transaction.'})
            data = DronePurpose.objects.get(id=request.GET['id'])
            data.delete()
            return JsonResponse({'success': True, 'url': '/masters/purpose/'}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=200)

class PurposeAdd(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Purpose Add"""
    @method_decorator(permission_decorator(permission='purpose-save'))
    def post(self, request):
        """Purpose Add Post"""
        try:
            form = SavePurposeForm(request.POST)
            if form.is_valid():
                name = request.POST['txt_name']
                description = request.POST['description']
                # purpose_check = DronePurpose.objects.filter(name=name).count()
                # if purpose_check:
                #     return JsonResponse({'success': 'exist', 'msg': 'Sorry! Drone Purpose already exist.'})
                purpose = DronePurpose(
                name=name,
                description = description,
                created_by = request.user
                )
                purpose.save()
                return JsonResponse({'success': True, 'msg': 'Successfully Added'}, status=200)
            return JsonResponse({'success': False, 'errors': form.errors}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=500)

class PurposeUpdate(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Purpose Update"""
    @method_decorator(permission_decorator(permission='purpose-update'))
    def post(self, request):
        """Purpose Update Post"""
        try:
            form = UpdatePurposeForm(request.POST)
            if form.is_valid():
                name = request.POST['txt_name']
                description = request.POST['description']
                purp_id = request.POST['purpId']
                # purpose_check = DronePurpose.objects.filter(name=name).exclude(id=purp_id).count()
                # if purpose_check:
                #     return JsonResponse({'success': 'exist', 'msg': 'Sorry! Drone Purpose already exist.'})
                purpose = DronePurpose.objects.get(id=purp_id)
                purpose.name = name
                purpose.description = description
                purpose.created_by = request.user
                purpose.save()
                return JsonResponse({'success': True, 'msg': 'Successfully Updated'}, status=200)
            return JsonResponse({'success': False, 'errors': form.errors}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=500)
