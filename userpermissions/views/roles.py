from userpermissions.models import RoleModel, GroupModel, RoleGroupModel, UserRoleModel, RoleGroupModel
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from userpermissions.decorators import permission_decorator
from userpermissions.form import SaveRoleForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.db.models import Q
from django.views import View
from utils import helper
import json
from django.conf import settings

TABLE_ROW_LIMIT = settings.TABLE_ROW_LIMIT

class MasterRoles(LoginRequiredMixin, View):
    @method_decorator(permission_decorator(permission='role-list'))
    def get(self, request):
        query_url = ''
        groups = GroupModel.objects.filter()
        # group_data = []
        # for group in groups:
        #     dt = {}
        #     dt["id"] = group.id
        #     dt["text"] = group.name
        #     group_data.append(dt)

        try:
            query = request.GET['search']
        except Exception as e:
            query = ''
        if query:
            roledata = RoleModel.objects.filter(
                Q(name__icontains=request.GET['search'])).order_by('name')
        else:
            roledata = RoleModel.objects.all().order_by('name')

        for rl in roledata:
            rl.selected_group = json.dumps(list(
                RoleGroupModel.objects.filter(role_id=rl.id).values_list('group_id', flat=True)))

        page = request.GET.get('page', 1)
        paginator = Paginator(roledata, TABLE_ROW_LIMIT)

        try:
            roles = paginator.page(page)
        except PageNotAnInteger:
            roles = paginator.page(1)
        except EmptyPage:
            roles = paginator.page(paginator.num_pages)
        if query:
            query_url = '&search='+query
        return render(request, 'user_roles.html', {'data': roledata, 'roles': roles, 'query': query, 'groups': (groups),'query_url':query_url})

    @method_decorator(permission_decorator(permission='add-role'))
    def post(self, request):
        try:
            json_data = request.body.decode("utf-8")
            data = json.loads(json_data)
            form = SaveRoleForm(data)
            if form.is_valid():
                role = data['role']
                description = data['description']
                groups = data['group']
                roleid = data['roleid'] and data['roleid'] or None

                role_model = RoleModel(
                    name=role,
                    description=description
                )
                role_model.save()

                RoleGroupModel.objects.filter(
                    role_id=role_model.id).delete()
                # Group to role
                for group in groups:
                    group_data = GroupModel.objects.get(id=group)
                    role_group_model = RoleGroupModel()
                    role_group_model.role_id = role_model
                    role_group_model.group_id = group_data
                    role_group_model.save()

                return JsonResponse({'success': True, 'msg': 'Successfully Added'}, status=200)
            else:
                return JsonResponse({'success': False, 'errors': form.errors}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'msg': str(e)}, status=500)

    @method_decorator(permission_decorator(permission='delete-role'))
    def delete(self, request):
        try:
            data = RoleModel.objects.get(id=request.GET['id'])
            relation_exist = self._check_relation(data.id)
            if relation_exist:
                return JsonResponse({'success': False, 'msg': "Unable to delete. Data relation exist!"}, status=200)

            data.delete()
            return JsonResponse({'success': True, 'url': '/permissions/roles/'}, status=200)
        except Exception as e:
            return JsonResponse({'success': True, 'msg': str(e)}, status=200)

    # CHECK RELATION
    # PRIVATE FUNCTION
    def _check_relation(self, id):
        user_roles = UserRoleModel.objects.filter(role_id=id).count()
        role_groups = RoleGroupModel.objects.filter(role_id=id).count()
        result = False
        if user_roles > 0 and role_groups > 0:
            result = True
        return result


class MasterUpdateRoles(LoginRequiredMixin, View):
    @method_decorator(permission_decorator(permission='edit-role'))
    def post(self, request):
        try:
            json_data = request.body.decode("utf-8")
            data = json.loads(json_data)
            form = SaveRoleForm(data)
            if form.is_valid():
                role = data['role']
                description = data['description']
                groups = data['group']
                roleid = data['roleid'] and data['roleid'] or None

                role_model = RoleModel.objects.get(id=roleid)
                role_model.name = role
                role_model.description = description
                role_model.save()

                RoleGroupModel.objects.filter(
                    role_id=role_model.id).delete()
                # Group to role
                for group in groups:
                    group_data = GroupModel.objects.get(id=group)
                    role_group_model = RoleGroupModel()
                    role_group_model.role_id = role_model
                    role_group_model.group_id = group_data
                    role_group_model.save()

                return JsonResponse({'success': True, 'msg': 'Successfully Updated'}, status=200)
            else:
                return JsonResponse({'success': False, 'errors': form.errors}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'msg': str(e)}, status=500)
