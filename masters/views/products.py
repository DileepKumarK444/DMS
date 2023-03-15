# pylint: disable=no-member
"""
Product Master
"""
# pylint: disable=E0401
import os
import json
import datetime
from ast import literal_eval

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.views import View
from django.core import serializers
from django.conf import settings

from masters.form import SaveProduct, UpdateProduct
from masters.models import ProductType, Category, Product, TransactionLog
from drone_management.models import DroneStatus
from userpermissions.decorators import permission_decorator

from utils.encryption import aes

encry = aes(settings.KEY, settings.IV)
ROOT_DIR = os.path.abspath(os.curdir)

BASE_URL = settings.BASE_URL
APP_NAME = settings.APP_NAME
DMS_URL = settings.DMS_URL
PURCHASE_LIMIT = settings.PURCHASE_LIMIT
TABLE_ROW_LIMIT = settings.TABLE_ROW_LIMIT

class Products(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Products"""
    @method_decorator(permission_decorator(permission='item-list'))
    def get(self, request):
        """Products Get"""
        query_url = ''
        # products = Product.objects.filter().values('id','serial_number','pur_date','trans_type','category__model','category__type__name','active','status','drone_status','note').order_by('-id')
        try:
            query = request.GET['search']
        except: # pylint: disable=W0702
            query = ''
        if query:
            customerdata = Products.filter(
                Q(serial_number__icontains=request.GET['search']) |
                Q(pur_date__icontains=request.GET["search"]) |
                Q(trans_type__icontains=request.GET["search"]) |
                Q(category__type__name__icontains=request.GET["search"]) |
                Q(category__model__icontains=request.GET["search"])
                ).values('id','serial_number','pur_date','trans_type','category__model','category__type__name','category','active','status','drone_status','note').order_by('-id')
        else:
            customerdata = Product.objects.filter().values('id','serial_number','pur_date','trans_type','category__model','category__type__name','category','active','status','drone_status','note').order_by('-id')
        page = request.GET.get('page', 1)
        paginator = Paginator(customerdata, TABLE_ROW_LIMIT)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        if query:
            query_url = '&search='+query
        drone_status = DroneStatus.objects.filter(type='Item')
        return render(request, 'products/list.html', {'drone_status':drone_status,'data': customerdata, 'products': products, 'query': query,'query_url':query_url})

    @method_decorator(permission_decorator(permission='item-delete'))
    def delete(self, request):
        """Products Delete"""
        try:
            cat_id = request.GET['catid']
            cat_check = Product.objects.filter(id=request.GET['id'],trans_type="Allocated").count()
            if cat_check:
                return JsonResponse({'success': 'exist', 'msg': 'Sorry can\'t delete, Item already allocated to a drone.'})
            cat = Category.objects.filter(id=cat_id).values('quantity')
            cat_data = Category.objects.get(id=cat_id)
            cat_data.quantity=int(cat[0]['quantity'])-1
            cat_data.save()
            del_st = DroneStatus.objects.get(id=request.GET['del'])
            Product.objects.filter(id=request.GET['id']).update(status=False,active=False,drone_status=del_st)
            return JsonResponse({'success': True, 'url': '/masters/products/'}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=200)

class ActivateDrone(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Activate Drone"""
    def post(self, request):
        """Activate Drone"""
        cid = request.POST['id']
        prod = Product.objects.get(id=cid)
        prod.status = True
        prod.active =True
        prod.drone_status = None
        prod.note = ''
        prod.save()
        return JsonResponse({'success': True, 'msg': 'Successfully Activated'}, status=200)

class ProductAdd(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Product Add"""
    @method_decorator(permission_decorator(permission='item-add'))
    def get(self, request):
        """Product Add Get"""
        product_type = ProductType.objects.all()
        return render(request, 'products/add.html', {'product_type': product_type,'PURCHASE_LIMIT':PURCHASE_LIMIT})

    @method_decorator(permission_decorator(permission='item-save'))
    def post(self, request):
        """Product"""
        try:
            form = SaveProduct(request.POST)
            if form.is_valid():
                cb_product_type = request.POST['cb_product_type']
                category = request.POST['cb_category']
                serial_number = request.POST['txt_serial_no']
                pur_date = datetime.datetime.strptime(str(request.POST['dt_purchase']), '%Y-%m-%d')
                trans_type = 'New'
                serial_nos = serial_number.split(',')
                cat = Category.objects.get(id = category)
                description = 'Added new '+str(len(serial_nos))+' datas - Transaction date: '+str(pur_date)+',serial nos :'+str(serial_nos)
                for serial_no in serial_nos:
                    try:
                        serial_no_check = Product.objects.filter(serial_number=serial_no,category=category).count()
                        if serial_no_check:
                            return JsonResponse({'success': 'exist', 'msg': 'Sorry! serial number(s) already exist.'})
                    except: # pylint: disable=W0702
                        pass
                    prod = Product(
                        category=cat,
                        serial_number = serial_no,
                        pur_date = pur_date,
                        trans_type = trans_type,
                    )
                    prod.save()
                cat = Category.objects.filter(id=category).values('quantity')
                cat_data = Category.objects.get(id=category)
                if cat[0]['quantity']=='':
                    cat_data.quantity=len(serial_nos)
                else:
                    cat_data.quantity=len(serial_nos)+int(cat[0]['quantity'])
                cat_data.save()
                prod_type = ProductType.objects.get(id = cb_product_type)
                trans_log = TransactionLog(
                    category=cat_data,
                    type = prod_type,
                    quantity = len(serial_nos),
                    action = 'add',
                    date = pur_date,
                    description = description,
                    trans_type = trans_type,
                )
                trans_log.save()
                return JsonResponse({'success': True, 'msg': 'Successfully Added'}, status=200)
            return JsonResponse({'success': False, 'errors': form.errors}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=500)

class GetDataCB(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Get Data CB"""
    def post(self, request):
        """Get Data CB"""
        try:
            json_data = request.body.decode("utf-8")
            data = json.loads(json_data)
            cat =''
            if data['id']:
                cat = serializers.serialize('json', Category.objects.filter(type=data['id']))
            return JsonResponse({'success': True, 'data': cat}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=500)

class ProductEdit(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Product Edit"""
    @method_decorator(permission_decorator(permission='item-edit'))
    def get(self, request,cid):
        """Product Edit Get"""
        prod = Product.objects.filter(id=cid).values()
        if prod[0]['status']:
            drone_status = DroneStatus.objects.filter(type='Item')
            product_type = ProductType.objects.all()
            products = Product.objects.get(id=cid)
            return render(request, 'products/edit.html', {'product_type': product_type,'products':products,'id':cid,'PURCHASE_LIMIT':PURCHASE_LIMIT, 'drone_status':drone_status})
        return redirect('/masters/products/')

class ProductUpdate(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Product Update"""
    @method_decorator(permission_decorator(permission='item-update'))
    def post(self, request):
        """Product Update Post"""
        try:
            form = UpdateProduct(request.POST)
            if form.is_valid():
                prod_id = request.POST['hd_id']
                old_cat = request.POST['hd_old_cat']
                category = request.POST['cb_category']
                pur_date = request.POST['dt_purchase']
                serial_number = request.POST['txt_serial_no']
                status = literal_eval(request.POST['status'])
                del_st = request.POST['del_st']
                cat_check = Product.objects.filter(id=prod_id,trans_type="Allocated").count()
                if cat_check:
                    return JsonResponse({'success': 'exist', 'msg': 'Sorry can\'t edit, Item already allocated to a drone.'})
                ta_note = ''
                drone_status = None
                if not status:
                    drone_status = DroneStatus.objects.get(id=del_st)
                ta_note = request.POST['ta_note']
                prod_type = request.POST['cb_product_type']
                cat_old_data = Category.objects.get(id=old_cat)
                cat_new_data = Category.objects.get(id=category)
                prod_type_obj = ProductType.objects.get(id = prod_type)
                if old_cat != category:
                    cat_old = Category.objects.filter(id=old_cat).values('quantity','model')
                    cat_new = Category.objects.filter(id=category).values('quantity','model')
                    cat_old_data.quantity=cat_old[0]['quantity']-1
                    cat_old_data.save()
                    description = 'Removed one data from '+cat_old[0]['model']+' - Transaction date: '+str(pur_date)
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
                    description = 'Added one data to '+cat_new[0]['model']+' - Transaction date: '+str(pur_date)
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
                prod.active = status
                prod.note = ta_note
                prod.drone_status = drone_status
                prod.pur_date = pur_date
                prod.trans_type = 'New'
                prod.save()
                return JsonResponse({'success': True, 'msg': 'Updated successfully'}, status=200)
            return JsonResponse({'success': False, 'errors': form.errors}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=500)

class GetData(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Get Data"""
    def post(self, request):
        """Get Data Post"""
        try:
            prod_id = request.POST['id']
            products = list(Product.objects.filter(id=prod_id).values('id','serial_number','pur_date','trans_type','category','category__type__id','status','drone_status','note','active'))
            cat = serializers.serialize('json', Category.objects.filter(type=products[0]['category__type__id']))
            return JsonResponse({'success': True, 'data': products,'cat':cat}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=500)
