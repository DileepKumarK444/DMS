from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from userpermissions.models import GroupModel, GroupPermissionModel, RoleGroupModel
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from userpermissions.form import SaveGroupForm
import json
from django.db.models import Q
from userpermissions.decorators import permission_decorator
from django.utils.decorators import method_decorator
from utils import helper
from django.conf import settings

TABLE_ROW_LIMIT = settings.TABLE_ROW_LIMIT

class MasterGroup(LoginRequiredMixin, View):
    @method_decorator(permission_decorator(permission='group-list'))
    def get(self, request):
        query_url = ''
        try:
            query = request.GET['search']
        except Exception as e:
            query = ''
        if query:
            groupdata = GroupModel.objects.filter(
                Q(name__icontains=request.GET['search'])).order_by('name')
        else:
            groupdata = GroupModel.objects.all().order_by('name')
        page = request.GET.get('page', 1)
        paginator = Paginator(groupdata, TABLE_ROW_LIMIT)

        try:
            groups = paginator.page(page)
        except PageNotAnInteger:
            groups = paginator.page(1)
        except EmptyPage:
            groups = paginator.page(paginator.num_pages)
        if query:
            query_url = '&search='+query
        return render(request, 'group.html', {'data': groupdata, 'groups': groups, 'query': query,'query_url':query_url})

    @method_decorator(permission_decorator(permission='add-group'))
    def post(self, request):
        try:
            form = SaveGroupForm(request.POST)
            if form.is_valid():
                group = request.POST['group']
                description = request.POST['description']
                groupid = request.POST.get(
                    'groupid') and request.POST.get('groupid') or None

                input = GroupModel(
                    name=group,
                    description=description
                )
                input.save()
                return HttpResponse(json.dumps({'success': True, 'msg': 'Successfully Added'}), status=200)
            else:
                return HttpResponse(json.dumps({'success': False, 'errors': form.errors}), status=200)
        except Exception as e:
            return HttpResponse(json.dumps({'success': False, 'msg': str(e)}), status=500)

    @method_decorator(permission_decorator(permission='delete-group'))
    def delete(self, request):
        try:
            data = GroupModel.objects.get(id=request.GET['id'])
            is_exist = self._check_relation(data.id)
            if is_exist:
                return JsonResponse({'success': False, 'msg': "Unable to delete. Data relation exist!"}, status=200)

            data.delete()
            return JsonResponse({'success': True, 'url': '/permissions/group/'}, status=200)
        except Exception as e:
            return HttpResponse(json.dumps({'success': True, 'msg': str(e)}), status=200)

    # CHECK RELATION EXIST
    # PRIVATE FUNCTION
    def _check_relation(self, id):
        group_permissions = GroupPermissionModel.objects.filter(
            group_id=id).count()
        role_groups = RoleGroupModel.objects.filter(group_id=id).count()
        result = False
        if group_permissions > 0 or role_groups > 0:
            result = True
        return result


class MasterUpdateGroup(LoginRequiredMixin, View):
    @method_decorator(permission_decorator(permission='edit-group'))
    def post(self, request):
        try:
            form = SaveGroupForm(request.POST)
            if form.is_valid():
                group = request.POST['group']
                description = request.POST['description']
                groupid = request.POST.get(
                    'groupid') and request.POST.get('groupid') or None

                input = GroupModel.objects.get(id=groupid)
                input.name = group
                input.description = description
                input.save()

                return HttpResponse(json.dumps({'success': True, 'msg': 'Successfully Updated'}), status=200)
            else:
                return HttpResponse(json.dumps({'success': False, 'errors': form.errors}), status=200)
        except Exception as e:
            return HttpResponse(json.dumps({'success': False, 'msg': str(e)}), status=500)
