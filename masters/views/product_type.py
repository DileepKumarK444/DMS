# pylint: disable=no-member
"""
Product Type Master
"""
# pylint: disable=E0401
import os
import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from django.views import View
from django.core import serializers
from django.conf import settings

from utils.encryption import aes

from masters.form import SaveProductType, UpdateProductType
from masters.models import ProductType, Category

from userpermissions.decorators import permission_decorator

encry = aes(settings.KEY, settings.IV)
ROOT_DIR = os.path.abspath(os.curdir)
BASE_URL = settings.BASE_URL
APP_NAME = settings.APP_NAME
DMS_URL = settings.DMS_URL
TABLE_ROW_LIMIT = settings.TABLE_ROW_LIMIT

class ProductTypeList(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Product Type List"""
    @method_decorator(permission_decorator(permission='product-type-list'))
    def get(self, request):
        """Product Type List Get"""
        query_url = ''
        # product_type = ProductType.objects.filter().order_by('-id')
        try:
            query = request.GET['search']
        except: # pylint: disable=W0702
            query = ''
        if query:
            producttypedata = ProductType.objects.filter(
                Q(name__icontains=request.GET['search']) |
                Q(description__icontains=request.GET["search"])
                ).order_by('-id')
        else:
            producttypedata = ProductType.objects.all().order_by('-id')
        page = request.GET.get('page', 1)
        paginator = Paginator(producttypedata, TABLE_ROW_LIMIT)
        try:
            product_type = paginator.page(page)
        except PageNotAnInteger:
            product_type = paginator.page(1)
        except EmptyPage:
            product_type = paginator.page(paginator.num_pages)
        if query:
            query_url = '&search='+query
        return render(request, 'product_type/list.html', {'data': producttypedata, 'query': query, 'product_type': product_type,'query_url':query_url,'msg':''})

    @method_decorator(permission_decorator(permission='product-type-delete'))
    def delete(self, request):
        """Product Type List Delete"""
        try:
            type_check = Category.objects.filter(type=request.GET['id']).count()
            if type_check:
                return JsonResponse({'success': 'exist', 'msg': 'Sorry can\'t delete, Product type already have transaction.'})
            data = ProductType.objects.get(id=request.GET['id'])
            data.delete()
            return JsonResponse({'success': True, 'url': '/masters/product_type/'}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=200)

class ProductTypeAdd(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Product Type Add"""
    @method_decorator(permission_decorator(permission='product-type-save'))
    def post(self, request):
        """Product Type Add Post"""
        try:
            form = SaveProductType(request.POST)
            if form.is_valid():
                name = request.POST['txt_name']
                description = request.POST['description']
                status = True
                cb_type = request.POST['cb_type']
                # type_check = ProductType.objects.filter(name=name).count()
                # if type_check:
                #     return JsonResponse({'success': 'exist', 'msg': 'Sorry! Product type already exist.'})
                prod = ProductType(
                    name=name,
                    description = description,
                    active = status,
                    type=cb_type
                )
                prod.save()
                return JsonResponse({'success': True, 'msg': 'Successfully Added'}, status=200)
            return JsonResponse({'success': False, 'errors': form.errors}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=500)

class ProductTypeUpdate(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Product Type Update"""
    @method_decorator(permission_decorator(permission='product-type-update'))
    def post(self, request):
        """Product Type Update Post"""
        try:
            form = UpdateProductType(request.POST)
            if form.is_valid():
                name = request.POST['txt_name']
                description = request.POST['description']
                status = True
                type_id = request.POST['typeid']
                cb_type = request.POST['cb_type']
                # type_check = ProductType.objects.filter(name=name).exclude(id=type_id).count()
                # if type_check:
                #     return JsonResponse({'success': 'exist', 'msg': 'Sorry! Product type already exist.'})
                prod_type = ProductType.objects.get(id=type_id)
                prod_type.name = name
                prod_type.description = description
                prod_type.active = status
                prod_type.type = cb_type
                prod_type.save()
                return JsonResponse({'success': True, 'msg': 'Successfully Updated'}, status=200)
            return JsonResponse({'success': False, 'errors': form.errors}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=500)

class GetDataCB(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Get Data CB"""
    def post(self, request):
        """Get Data CB Post"""
        try:
            json_data = request.body.decode("utf-8")
            data = json.loads(json_data)
            cat =''
            if data['id']:
                cat = serializers.serialize('json', Category.objects.filter(type=data['id']))
            return JsonResponse({'success': True, 'data': cat}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=500)
