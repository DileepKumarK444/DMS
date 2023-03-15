import logging
from re import sub
from django.http import JsonResponse
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin
from rest_framework.authtoken.models import Token
# Permission.objects.filter(permissiongroup__role=self.filter(user=user).first().role)
from userpermissions.models import  UserRoleModel, GroupPermissionModel, RoleGroupModel
from masters.models import Customer, CustomerUser, ConsumptionLog
from django.conf import settings
import datetime
from django.db.models import Q


class SelectorMiddleware(MiddlewareMixin):

    def process_request(self, request):
        now = datetime.datetime.now()
        

        cpu_usage = ConsumptionLog.objects.filter(status =  'Unread', cpu_usage__gte = 80).values()
        request.cpu_usage = cpu_usage.count()

        swap_memory = ConsumptionLog.objects.filter(status =  'Unread', swap_memory__gte = 80).values()
        request.swap_memory = swap_memory.count()

        virtual_memory = ConsumptionLog.objects.filter(status =  'Unread', virtual_memory__gte = 80).values()
        request.virtual_memory = virtual_memory.count()

        header_token = request.META.get('HTTP_AUTHORIZATION', None)
        user = ''
        request.role = ''
        request.permissions =''
        request.customer_id = ''
        request.permissions = []
        if header_token is not None:
            try:
                token = sub('Token ', '', request.META.get(
                    'HTTP_AUTHORIZATION', None))
                token_obj = Token.objects.get(key=token)
                user = token_obj.user
                request.user = user
                request.email = user.email
                
                if not user.is_superuser:
                    request.role = UserRoleModel.objects.filter(user_id=user).values_list('role_id__name', flat=True)[0]
                    request.permissions = GroupPermissionModel.objects.filter(group_id=RoleGroupModel.objects.filter(role_id=UserRoleModel.objects.filter(user_id=user).first().role_id).first().group_id).values_list('permission_id__code', flat=True)
                    request.customer_id = Customer.objects.filter(id=CustomerUser.objects.filter(email = user.email).first().customer_id).values_list('customer_id', flat=True)
                    request.customer_name = Customer.objects.filter(id=CustomerUser.objects.filter(email = user.email).first().customer_id).values_list('account_name', flat=True)
                    # print('request.customer_id',request.customer_id)
                # else:
                #     return JsonResponse({'status':False, "msg":"Please use customer Admin/User"},
                #                     status=200)   
                # print('request.user',request.user)
                # print('request.customer_id',request)
            except Token.DoesNotExist:
                pass
        
