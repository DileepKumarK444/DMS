# pylint: disable=no-member
"""
Subset Templat Master
"""
# pylint: disable=E0401
import os
import pandas
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from django.views import View
from django.conf import settings
from masters.models import LogTemplate
from masters.form import SaveTemplate, GetFieldsForm,UpdateTemplate
from utils.encryption import aes
from userpermissions.decorators import permission_decorator

encry = aes(settings.KEY, settings.IV)
ROOT_DIR = os.path.abspath(os.curdir)
BASE_URL = settings.BASE_URL
APP_NAME = settings.APP_NAME
DMS_URL = settings.DMS_URL
PURCHASE_LIMIT = settings.PURCHASE_LIMIT
TABLE_ROW_LIMIT = settings.TABLE_ROW_LIMIT

class TemplateList(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Template List"""
    @method_decorator(permission_decorator(permission='log-fields-template-list'))
    def get(self, request):
        """Template List Get"""
        query_url = ''
        # templates = LogTemplate.objects.filter().values().order_by('-id')
        try:
            query = request.GET['search']
        except: # pylint: disable=W0702
            query = ''
        if query:
            templatedata = LogTemplate.objects.filter(
                Q(template_name__icontains=request.GET['search'])).values().order_by('-id')
        else:
            templatedata = LogTemplate.objects.filter().values().order_by('-id')
        page = request.GET.get('page', 1)
        paginator = Paginator(templatedata, TABLE_ROW_LIMIT)
        try:
            templates = paginator.page(page)
        except PageNotAnInteger:
            templates = paginator.page(1)
        except EmptyPage:
            templates = paginator.page(paginator.num_pages)
        if query:
            query_url = '&search='+query
        return render(request, 'log_fields_template/list.html',{'templates':templates,'query':query,'query_url':query_url})

    @method_decorator(permission_decorator(permission='log-fields-template-delete'))
    def delete(self, request):
        """Template List Delete"""
        try:
            data = LogTemplate.objects.get(id=request.GET['id'])
            data.delete()
            return JsonResponse({'success': True, 'url': '/masters/log_field_template/list/'}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=200)

class TemplateAdd(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Template Add"""
    @method_decorator(permission_decorator(permission='log-fields-template-add'))
    def get(self, request):
        """Template Add Get"""
        return render(request, 'log_fields_template/add.html')

class GetFields(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Get Fields"""
    def post(self, request):
        """Get Fields Post"""
        file = request.FILES.get('txt_file')
        form = GetFieldsForm(request.POST,request.FILES)
        if form.is_valid():
            data = pandas.read_csv(file)
            data_frame = pandas.DataFrame(data)
            list_of_column_names = list(data_frame.columns)
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=200)
        return JsonResponse({'success': True, 'msg': 'Successfully Added','data':list_of_column_names}, status=200)

class SaveFields(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Save Fields"""
    @method_decorator(permission_decorator(permission='log-fields-template-save'))
    def post(self, request):
        """Save Fields Post"""
        try:
            form = SaveTemplate(request.POST)
            if form.is_valid():
                txt_template_name = request.POST['txt_template_name']
                log_fields = request.POST['log_fields']
                # log_temp_check = LogTemplate.objects.filter(template_name=txt_template_name).count()
                # if log_temp_check:
                #     return JsonResponse({'success': 'exist', 'msg': 'Sorry! Template already exist.'})
                log_temp = LogTemplate(
                    template_name=txt_template_name,
                    log_fields = log_fields
                    )
                log_temp.save()
                return JsonResponse({'success': True, 'msg': 'Successfully Saved'}, status=200)
            return JsonResponse({'success': False, 'errors': form.errors}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=500)

class UpdateFields(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Update Fields"""
    @method_decorator(permission_decorator(permission='log-fields-template-update'))
    def post(self, request):
        """Update Fields Post"""
        try:
            form = UpdateTemplate(request.POST)
            if form.is_valid():
                txt_template_name = request.POST['txt_template_name']
                log_fields = request.POST['log_fields']
                log_id = request.POST['id']
                # log_temp_check = LogTemplate.objects.filter(template_name=txt_template_name).exclude(id=log_id).count()
                # if log_temp_check:
                #     return JsonResponse({'success': 'exist', 'msg': 'Sorry! Template already exist.'})
                log_temp = LogTemplate.objects.get(id = log_id)
                log_temp.template_name=txt_template_name
                log_temp.log_fields = log_fields
                log_temp.save()
                return JsonResponse({'success': True, 'msg': 'Successfully Updated'}, status=200)
            return JsonResponse({'success': False, 'errors': form.errors}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=500)

class EditFields(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Edit Fields"""
    @method_decorator(permission_decorator(permission='log-fields-template-edit'))
    def get(self, request,cid):
        """Edit Fields Get"""
        try:
            log_temp = LogTemplate.objects.get(id=cid)
            return render(request, 'log_fields_template/edit.html', {'logTemp': log_temp,'id':cid})
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=500)

class GetData(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Get Data"""
    def post(self, request):
        """Get Data Post"""
        try:
            log_id = request.POST['id']
            log_temp = list(LogTemplate.objects.filter(id=log_id).values())
            return JsonResponse({'success': True, 'logTemp': log_temp}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=500)
