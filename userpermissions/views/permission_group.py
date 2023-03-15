from userpermissions.models import PermissionModel, GroupModel, GroupPermissionModel
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from userpermissions.form import SaveGroupPermissionForm
from django.utils.decorators import method_decorator
from userpermissions.decorators import permission_decorator
from django.template.defaultfilters import slugify
from django.http import HttpResponse
from django.shortcuts import render
from utils import helper
from django.db.models import Q
from django.views import View
import json
from django.conf import settings

TABLE_ROW_LIMIT = settings.TABLE_ROW_LIMIT

class MasterPermission(LoginRequiredMixin, View):
    @method_decorator(permission_decorator(permission='permission-group-list'))
    def get(self, request):

        all_group = GroupModel.objects.all().order_by('name').values()
        for group in all_group:
            group['permissions'] = list(GroupPermissionModel.objects.filter(group_id=group['id']).values_list(
                'permission_id', flat=True))

        all_permissions = PermissionModel.objects.all().order_by('name')

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
        return render(request, 'permission_group.html', {'data': permissiondata, 'permissions': permissions, 'query': query, 'all_group': all_group, 'all_permissions': all_permissions})

    @method_decorator(permission_decorator(permission='permission-group-list'))
    def post(self, request):
        try:
            form = SaveGroupPermissionForm(request.POST)
            if form.is_valid():
                permission_id = request.POST['permission_id']
                group_id = request.POST['group_id']
                object_count = GroupPermissionModel.objects.filter(
                    group_id=group_id, permission_id=permission_id).count()
                if object_count > 0:
                    GroupPermissionModel.objects.filter(
                        group_id=group_id, permission_id=permission_id).delete()

                else:
                    permission = PermissionModel.objects.get(
                        id=permission_id)
                    group = GroupModel.objects.get(
                        id=group_id)
                    group_permission = GroupPermissionModel()
                    group_permission.permission_id = permission
                    group_permission.group_id = group
                    group_permission.save()

                return HttpResponse(json.dumps({'success': True, 'msg': 'Successfully Updated'}), status=200)
            else:
                return HttpResponse(json.dumps({'success': False, 'errors': form.errors}), status=200)
        except Exception as e:
            return HttpResponse(json.dumps({'success': False, 'msg': str(e)}), status=500)
