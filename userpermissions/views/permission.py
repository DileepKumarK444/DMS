from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from userpermissions.models import PermissionModel, GroupPermissionModel
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from userpermissions.form import SavePermissionForm
import json
from django.db.models import Q
from django.template.defaultfilters import slugify
from userpermissions.decorators import permission_decorator
from django.utils.decorators import method_decorator
from utils import helper
from django.conf import settings

TABLE_ROW_LIMIT = settings.TABLE_ROW_LIMIT

class MasterPermission(LoginRequiredMixin, View):
    @method_decorator(permission_decorator(permission='permission-list'))
    def get(self, request):
        query_url = ''
        try:
            query = request.GET['search']
        except Exception as e:
            query = ''
        if query:
            permissiondata = PermissionModel.objects.filter(
                Q(name__icontains=request.GET['search']) | Q(code__icontains=request.GET['search']) | Q(description__icontains=request.GET['search'])).order_by('name')
        else:
            permissiondata = PermissionModel.objects.all().order_by('name')
        page = request.GET.get('page', 1)
        paginator = Paginator(permissiondata, TABLE_ROW_LIMIT)

        try:
            permissions = paginator.page(page)
        except PageNotAnInteger:
            permissions = paginator.page(1)
        except EmptyPage:
            permissions = paginator.page(paginator.num_pages)
        if query:
            query_url = '&search='+query
        return render(request, 'permission.html', {'data': permissiondata, 'permissions': permissions, 'query': query,"query_url":query_url})

    @method_decorator(permission_decorator(permission='add-permission'))
    def post(self, request):
        try:
            form = SavePermissionForm(request.POST)
            if form.is_valid():
                permission = request.POST['permission']
                description = request.POST['description']
                permissionid = request.POST.get(
                    'permissionid') and request.POST.get('permissionid') or None

                slug = slugify(permission.lower())
                isExist = PermissionModel.objects.filter(code=slug)
                if (len(isExist)):
                    return JsonResponse({'success': False, 'msg': 'Permission already exist!'}, status=400)

                input = PermissionModel(
                    name=permission,
                    code=slug,
                    description=description
                )
                input.save()

                return HttpResponse(json.dumps({'success': True, 'msg': 'Successfully Added'}), status=200)
            else:
                return HttpResponse(json.dumps({'success': False, 'errors': form.errors}), status=200)
        except Exception as e:
            return HttpResponse(json.dumps({'success': False, 'msg': str(e)}), status=500)

    @method_decorator(permission_decorator(permission='delete-permission'))
    def delete(self, request):
        try:
            data = PermissionModel.objects.get(id=request.GET['id'])
            group_permissions = GroupPermissionModel.objects.filter(
                permission_id=data.id).count()
            if group_permissions > 0:
                return JsonResponse({'success': False, 'msg': "Unable to delete. Data relation exist!"}, status=200)

            data.delete()
            return HttpResponse(json.dumps({'success': True, 'url': '/permissions/manage/'}), status=200)
        except Exception as e:
            return HttpResponse(json.dumps({'success': True, 'msg': str(e)}), status=200)


class MasterUpdatePermission(LoginRequiredMixin, View):
    @method_decorator(permission_decorator(permission='edit-permission'))
    def post(self, request):
        try:
            form = SavePermissionForm(request.POST)
            if form.is_valid():
                permission = request.POST['permission']
                description = request.POST['description']
                permissionid = request.POST.get(
                    'permissionid') and request.POST.get('permissionid') or None

                slug = slugify(permission.lower())
                isExist = PermissionModel.objects.filter(
                    Q(code=slug), ~Q(id=permissionid))
                if (len(isExist)):
                    return JsonResponse({'success': False, 'msg': 'Permission already exist!'}, status=400)

                input = PermissionModel.objects.get(id=permissionid)
                input.name = permission
                input.description = description
                input.save()

                return HttpResponse(json.dumps({'success': True, 'msg': 'Successfully Updated'}), status=200)
            else:
                return HttpResponse(json.dumps({'success': False, 'errors': form.errors}), status=200)
        except Exception as e:
            return HttpResponse(json.dumps({'success': False, 'msg': str(e)}), status=500)
