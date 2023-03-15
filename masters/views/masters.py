# # from userpermissions.models import RoleModel, GroupModel, RoleGroupModel, UserRoleModel, RoleGroupModel
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.utils.decorators import method_decorator
# from userpermissions.decorators import permission_decorator
# # from userpermissions.form import SaveRoleForm
# from django.http import HttpResponse, JsonResponse
# from django.shortcuts import render
# from django.db.models import Q
# from django.views import View
# from utils import helper
# import json
# from django.core import serializers
# from masters.models import Company, Country, State, Designation, Customer, CustomerUser, Drone, DroneAllocation, DashboardData, Plan
# import datetime
# from masters.form import SaveCustomer, SaveCustomerUser
# from django.contrib.auth.models import User
# # from django.contrib.auth.hashers import make_password
# from utils import helper
# import os

# from utils.encryption import aes
# from django.conf import settings
# from django.template import loader
# from masters.models import DmsSetting
# from userpermissions.models import RoleModel, UserRoleModel
# from django.core.mail import send_mail
# encry = aes(settings.KEY, settings.IV)
# ROOT_DIR = os.path.abspath(os.curdir)

# BASE_URL = settings.BASE_URL
# APP_NAME = settings.APP_NAME
# DMS_URL = settings.DMS_URL
# TABLE_ROW_LIMIT = settings.TABLE_ROW_LIMIT
# class Masters(LoginRequiredMixin, View):
#     @method_decorator(permission_decorator(permission='customer-list'))
#     def get(self, request):
#         query_url = ''
#         customers = Customer.objects.filter()
#         try:
#             query = request.GET['search']
#         except Exception as e:
#             query = ''
#         if query:
#             customerdata = Customer.objects.filter(
#                 Q(first_name__icontains=request.GET['search']) |
#                 Q(last_name__icontains=request.GET["search"]) |
#                 Q(email__icontains=request.GET["search"]) |
#                 Q(phone__icontains=request.GET["search"])
#                 )
#         else:
#             customerdata = Customer.objects.all()

#         page = request.GET.get('page', 1)
#         paginator = Paginator(customerdata, TABLE_ROW_LIMIT)

#         try:
#             customers = paginator.page(page)
#         except PageNotAnInteger:
#             customers = paginator.page(1)
#         except EmptyPage:
#             customers = paginator.page(paginator.num_pages)
#         if query:
#             query_url = '&search='+query
#         customers = ''
#         return render(request, 'main/list.html', {'data': customerdata, 'customers': customers, 'query': query, 'customers': (customers),'query_url':query_url})

# class MastersAdd(LoginRequiredMixin, View):
#     @method_decorator(permission_decorator(permission='add-customer'))
#     def get(self, request):
#         company = Company.objects.all()
#         country = Country.objects.all()
#         designation = Designation.objects.all()
#         return render(request, 'main/add.html', {'company': company, 'country': country, 'designation': designation})
