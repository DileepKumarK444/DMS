# pylint: disable=no-member
"""
Reason Master
"""
# pylint: disable=E0401
import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator

from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from django.views import View
from django.conf import settings

from masters.form import SaveReason,UpdateReason
from masters.models import DmsSetting, Product
from drone_management.models import DroneStatus, Drone
from userpermissions.decorators import permission_decorator

TABLE_ROW_LIMIT = settings.TABLE_ROW_LIMIT

class ReasonList(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Reason List"""
    @method_decorator(permission_decorator(permission='reason-list'))
    def get(self, request):
        """Reason List Get"""
        query_url = ''
        # reason = DroneStatus.objects.filter().values().order_by('-id')
        try:
            query = request.GET['search']
        except: # pylint: disable=W0702
            query = ''
        if query:
            reasondata = DroneStatus.objects.filter(
                Q(status__icontains=request.GET['search']) |
                Q(type__icontains=request.GET['search'])
                ).values().order_by('-id')
        else:
            reasondata = DroneStatus.objects.filter().values().order_by('-id')
        page = request.GET.get('page', 1)
        paginator = Paginator(reasondata, TABLE_ROW_LIMIT)
        try:
            reason = paginator.page(page)
        except PageNotAnInteger:
            reason = paginator.page(1)
        except EmptyPage:
            reason = paginator.page(paginator.num_pages)
        if query:
            query_url = '&search='+query
        modules = DmsSetting.objects.filter(conf_key='reason_module').values()
        return render(request, 'reason/list.html', {'data': reasondata, 'query': query, 'reason': reason,'query_url':query_url,'modules':json.loads(modules[0]['conf_value'])})

    @method_decorator(permission_decorator(permission='reason-delete'))
    def delete(self, request):
        """Reason List Delete"""
        try:
            reason_check_product = Product.objects.filter(drone_status=request.GET['id']).count()
            if reason_check_product:
                return JsonResponse({'success': 'exist', 'msg': 'Sorry can\'t delete, Reason already have transaction in Product.'})
            reason_check_drone = Drone.objects.filter(drone_status=request.GET['id']).count()
            if reason_check_drone:
                return JsonResponse({'success': 'exist', 'msg': 'Sorry can\'t delete, Reason already have transaction in Drone.'})
            data = DroneStatus.objects.get(id=request.GET['id'])
            data.delete()
            return JsonResponse({'success': True, 'url': '/masters/reason/'}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=200)

class ReasonAdd(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Reason Add"""
    @method_decorator(permission_decorator(permission='reson-add'))
    def post(self, request):
        """Reason Add Post"""
        try:
            form = SaveReason(request.POST)
            if form.is_valid():
                txt_reason = request.POST['txt_reason']
                module = request.POST['cb_module']
                # reason_check = DroneStatus.objects.filter(status=txt_reason,type = module).count()
                # if reason_check:
                #     return JsonResponse({'success': 'exist', 'msg': 'Sorry! Reason already exist.'})
                reason = DroneStatus(
                status = txt_reason,
                type = module
                )
                reason.save()
                return JsonResponse({'success': True, 'msg': 'Successfully Added'}, status=200)
            return JsonResponse({'success': False, 'errors': form.errors}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=500)

class ReasonUpdate(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Reason Update"""
    @method_decorator(permission_decorator(permission='reson-update'))
    def post(self, request):
        """Reason Update Post"""
        try:
            form = UpdateReason(request.POST)
            if form.is_valid():
                reason_id = request.POST['hd_id']
                txt_reason = request.POST['txt_reason']
                module = request.POST['cb_module']
                # reason_check = DroneStatus.objects.filter(status=txt_reason,type = module).exclude(id=reason_id).count()
                # if reason_check:
                #     return JsonResponse({'success': 'exist', 'msg': 'Sorry! Reason already exist.'})
                reason = DroneStatus.objects.get(id=reason_id)
                reason.status = txt_reason
                reason.type = module
                reason.save()
                return JsonResponse({'success': True, 'msg': 'Successfully Updated'}, status=200)
            return JsonResponse({'success': False, 'errors': form.errors}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=500)
    