# pylint: disable=no-member
"""
Settings Master
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

from masters.form import SaveSettingsForm, UpdateSettingsForm
from masters.models import DmsSetting, DmsBuildLog
from userpermissions.decorators import permission_decorator

from utils.encryption import aes

encry = aes(settings.KEY, settings.IV)
ROOT_DIR = os.path.abspath(os.curdir)

BASE_URL = settings.BASE_URL
APP_NAME = settings.APP_NAME
DMS_URL = settings.DMS_URL
TABLE_ROW_LIMIT = settings.TABLE_ROW_LIMIT

class SettingsList(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Settings List"""
    @method_decorator(permission_decorator(permission='settings-list'))
    def get(self, request):
        """Settings List Get"""
        query_url = ''
        # setting = DmsSetting.objects.filter().order_by('-id')
        try:
            query = request.GET['search']
        except: # pylint: disable=W0702
            query = ''
        if query:
            settingsdata = DmsSetting.objects.filter(
                Q(name__icontains=request.GET['search']) |
                Q(description__icontains=request.GET["search"])
                ).order_by('-id')
        else:
            settingsdata = DmsSetting.objects.all().order_by('-id')
        page = request.GET.get('page', 1)
        paginator = Paginator(settingsdata, TABLE_ROW_LIMIT)
        try:
            setting = paginator.page(page)
        except PageNotAnInteger:
            setting = paginator.page(1)
        except EmptyPage:
            setting = paginator.page(paginator.num_pages)
        if query:
            query_url = '&search='+query
        return render(request, 'settings/list.html', {'data': settingsdata, 'query': query, 'settings': setting,'query_url':query_url})

    @method_decorator(permission_decorator(permission='settings-delete'))
    def delete(self, request):
        """Settings List Delete"""
        try:
            data = DmsSetting.objects.get(id=request.GET['id'])
            data.delete()
            return JsonResponse({'success': True, 'url': '/masters/settings/'}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=200)

class SettingsAdd(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Settings Add"""
    @method_decorator(permission_decorator(permission='settings-save'))
    def post(self, request):
        """Settings Add Post"""
        try:
            form = SaveSettingsForm(request.POST)
            if form.is_valid():
                conf_key = request.POST['conf_key']
                conf_value = request.POST['conf_value']
                description = request.POST['description']
                # key_check = DmsSetting.objects.filter(conf_key=conf_key).count()
                # if key_check:
                #     return JsonResponse({'success': 'exist', 'msg': 'Sorry! Settings already exist.'})
                setting = DmsSetting(
                conf_key=conf_key,
                conf_value = conf_value,
                conf_description = description
                )
                setting.save()
                return JsonResponse({'success': True, 'msg': 'Successfully Added'}, status=200)
            return JsonResponse({'success': False, 'errors': form.errors}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=500)

class SettingsUpate(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Settings Upate"""
    @method_decorator(permission_decorator(permission='settings-update'))
    def post(self, request):
        """Settings Upate Post"""
        try:
            form = UpdateSettingsForm(request.POST)
            if form.is_valid():
                conf_key = request.POST['conf_key']
                conf_value = request.POST['conf_value']
                description = request.POST['description']
                set_id = request.POST['setId']
                # key_check = DmsSetting.objects.filter(conf_key=conf_key).exclude(id=set_id).count()
                # if key_check:
                #     return JsonResponse({'success': 'exist', 'msg': 'Sorry! Settings already exist.'})
                prev_value = DmsSetting.objects.filter(conf_key=conf_key).values()
                if conf_key == 'ap_build_no':
                    build_log = DmsBuildLog(
                    build_no=prev_value[0]['conf_value'],
                    portal = 'Admin'
                    )
                    build_log.save()
                if conf_key == 'cp_build_no':
                    build_log = DmsBuildLog(
                    build_no=prev_value[0]['conf_value'],
                    portal = 'Customer'
                    )
                    build_log.save()

                setting = DmsSetting.objects.get(id=set_id)
                setting.conf_key = conf_key
                setting.conf_value = conf_value
                setting.conf_description = description
                setting.save()

                # DmsBuildLog
                return JsonResponse({'success': True, 'msg': 'Successfully Updated'}, status=200)
            return JsonResponse({'success': False, 'errors': form.errors}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=500)
