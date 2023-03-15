""" Category Views"""
import json
import os
# pylint: disable=E0401
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.db.models import Q
from django.views import View
from django.core import serializers
from django.conf import settings
from django.utils.decorators import method_decorator
# pylint: disable=E0401
from masters.form import SaveCategory, UpateCategory
from masters.models import ProductType, Category, Product, TransactionLog
from userpermissions.decorators import permission_decorator
import sys
import os
# encry = aes(settings.KEY, settings.IV)
ROOT_DIR = os.path.abspath(os.curdir)
BASE_URL = settings.BASE_URL
APP_NAME = settings.APP_NAME
DMS_URL = settings.DMS_URL
TABLE_ROW_LIMIT = settings.TABLE_ROW_LIMIT
WARRANTY_LIMIT = settings.WARRANTY_LIMIT
class CategoryList(LoginRequiredMixin, View):
    """Category List Class"""
    @method_decorator(permission_decorator(permission='category-list'))
    def get(self, request):
        """Get List Function"""
        query_url = ''
        # category = Category.objects.filter().values('id',
        #     'model', 'additional_feature', 'warranty_period',
        #     'quantity',   'type_id','type_id__name').order_by('-id')
        try:
            query = request.GET['search']
        except: # pylint: disable=bare-except
            query = ''
        if query:
            categorydata = Category.objects.filter(
                Q(model__icontains=request.GET['search']) |
                Q(additional_feature__icontains=request.GET['search']) |
                Q(warranty_period__icontains=request.GET['search']) |
                Q(quantity__icontains=request.GET["search"]) |
                Q(type_id__name__icontains=request.GET["search"])
                ).values('id', 'model', 'additional_feature',
                'warranty_period',  'quantity',   'type_id','type_id__name').order_by('-id')
        else:
            categorydata = Category.objects.filter().values('id',
                'model', 'additional_feature', 'warranty_period',
                'quantity',   'type_id','type_id__name').order_by('-id')
        page = request.GET.get('page', 1)
        paginator = Paginator(categorydata, TABLE_ROW_LIMIT)
        try:
            category = paginator.page(page)
        except PageNotAnInteger:
            category = paginator.page(1)
        except EmptyPage:
            category = paginator.page(paginator.num_pages)
        if query:
            query_url = '&search='+query
        product_type = ProductType.objects.all()
        return render(request, 'category/list.html', {
                'data': categorydata,
                'query': query,
                'category': category,
                'query_url':query_url,
                'product_type':product_type,
                'WARRANTY_LIMIT':WARRANTY_LIMIT,
                'msg':''
                })
    @method_decorator(permission_decorator(permission='category-delete'))
    def delete(self, request):
        """Category Delete Function"""
        try:
            prod_check = Product.objects.filter(category=request.GET['id']).count()
            if prod_check:
                return JsonResponse({
                    'success': 'exist',
                    'msg': 'Sorry can\'t delete, Product already have transaction.'
                    })
            data = Category.objects.get(id=request.GET['id'])
            data.delete()
            return JsonResponse({'success': True, 'url': '/masters/category/'}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=200)

class CategoryAdd(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Category Add Class"""
    @method_decorator(permission_decorator(permission='category-add'))
    def post(self, request):
        """Category Post Function"""
        print('skfdjflisjfsjdlkfjsl;dkfslkdjflsdjflksjdflksjdflkjsd')
        try:
            form = SaveCategory(request.POST)
            if form.is_valid():
                
                model = request.POST['txt_model']
                feature = request.POST['txt_add_feature']
                period = request.POST['txt_period']
                typ = ProductType.objects.get(id=request.POST['product_type'])
                # if(period=='' or period == 0):
                if period in ('',0):
                    warranty = False
                    period = 0
                else:
                    warranty = True
                # cat_check = Category.objects.filter(model=model,type = typ).count()
                # if cat_check:
                #     return JsonResponse({
                #         'success': 'exist',
                #         'msg': 'Sorry! Category already exist.'
                #         })
                cat = Category(
                    model = model,
                    type = typ,
                    additional_feature = feature,
                    warranty_period = period,
                    warranty = warranty,
                    quantity = 0
                )
                cat.save()
                return JsonResponse({
                    'success': True,
                    'msg': 'Successfully Added'
                    }, status=200)
            return JsonResponse({'success': False, 'errors': form.errors}, status=200)
        except Exception as error: # pylint: disable=W0703
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return JsonResponse({'success': False, 'msg': str(error)}, status=500)

class CategoryUpdate(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Category Update Class"""
    @method_decorator(permission_decorator(permission='category-update'))
    def post(self, request):
        """Category Post Update"""
        try:
            form = UpateCategory(request.POST)
            if form.is_valid():
                catid = request.POST['catid']
                model = request.POST['txt_model']
                feature = request.POST['txt_add_feature']
                period = request.POST['txt_period']
                prod_type = ProductType.objects.get(id=request.POST['product_type'])
                old_type = request.POST['old_product_type']
                if period in ('',0):
                    warranty = False
                    period = 0
                else:
                    warranty = True
                # cat_check = Category.objects.filter(
                #     model=model,
                #     type = prod_type).exclude(id=catid).count()
                # if cat_check:
                #     return JsonResponse({
                #         'success': 'exist',
                #         'msg': 'Sorry! Category already exist.'
                #         })
                if old_type != request.POST['product_type']:
                    prod_exist_check = Product.objects.filter(category=catid).count()
                    if prod_exist_check:
                        return JsonResponse({
                            'success': 'exist',
                            'msg': 'Sorry! Transaction exist.'
                            })

                cat = Category.objects.get(id=catid)
                cat.model = model
                cat.type = prod_type
                cat.additional_feature = feature
                cat.warranty_period = period
                cat.warranty = warranty
                cat.save()
                return JsonResponse({'success': True, 'msg': 'Successfully Updated'}, status=200)
            return JsonResponse({'success': False, 'errors': form.errors}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=500)
class GetDataCB(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Category get CB Data"""
    def post(self, request):
        """Category CB Data Function"""
        cat =''
        try:
            json_data = request.body.decode("utf-8")
            data = json.loads(json_data)
            if data['id']:
                cat = serializers.serialize('json', Category.objects.filter(type=data['id']))
            return JsonResponse({'success': True, 'data': cat}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=500)

class ProductEdit(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Product Edit Class"""
    @method_decorator(permission_decorator(permission='product-edit'))
    def get(self, request,cid):
        """Product Edit"""
        product_type = ProductType.objects.all()
        products = Product.objects.get(id=cid)
        return render(request,
            'products/edit.html',
            {'product_type': product_type,'products':products,'id':cid})
class ProductUpdate(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Product Update Class"""
    @method_decorator(permission_decorator(permission='product-update'))
    def post(self, request):
        """Product Update Function"""
        try:
            prod_id = request.POST['hd_id']
            old_cat = request.POST['hd_old_cat']
            category = request.POST['cb_category']
            pur_date = request.POST['dt_purchase']
            serial_number = request.POST['txt_serial_no']
            prod_type = request.POST['cb_product_type']
            cat_old_data = Category.objects.get(id=old_cat)
            cat_new_data = Category.objects.get(id=category)
            prod_type_obj = ProductType.objects.get(id = prod_type)
            if old_cat != category:
                cat_old = Category.objects.filter(id=old_cat).values('quantity','model')
                cat_new = Category.objects.filter(id=category).values('quantity','model')
                cat_old_data.quantity=cat_old[0]['quantity']-1
                cat_old_data.save()
                description = 'Removed one data from '+\
                    cat_old[0]['model']+\
                    ' - Transaction date: '+\
                    str(pur_date)
                trans_log = TransactionLog(
                    category=cat_old_data,
                    type = prod_type_obj,
                    quantity = 1,
                    action = 'Edit',
                    date = pur_date,
                    description = description,
                    trans_type = 'New',
                )
                trans_log.save()
                description = 'Added one data to '+\
                    cat_new[0]['model']+\
                        ' - Transaction date: '+\
                        str(pur_date)
                cat_new_data.quantity=cat_new[0]['quantity']+1
                cat_new_data.save()
                trans_log = TransactionLog(
                    category=cat_new_data,
                    type = prod_type_obj,
                    quantity = 1,
                    action = 'Edit',
                    date = pur_date,
                    description = description,
                    trans_type = 'New',
                )
                trans_log.save()
            prod = Product.objects.get(id = prod_id)
            prod.category=cat_new_data
            prod.serial_number = serial_number
            prod.pur_date = pur_date
            prod.trans_type = 'New'
            prod.save()
            return JsonResponse({
                'success': True,
                'msg': 'Updated successfully'
                }, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=500)

class GetData(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Get Data Function"""
    def post(self, request):
        """Get Data Function"""
        try:
            data_id = request.POST['id']
            products = list(Product.objects.filter(id=data_id).values('id',
                'serial_number','pur_date','trans_type','category',
                'category__type__id')
                )
            cat = serializers.serialize('json',
            Category.objects.filter(type=products[0]['category__type__id'])
            )
            return JsonResponse({'success': True, 'data': products,'cat':cat}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=500)
