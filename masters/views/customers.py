# pylint: disable=no-member
"""
Customer Master
"""
import os
import json
import datetime
# from urllib import request
# pylint: disable=E0401
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from django.views import View
from django.core import serializers
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader
from userpermissions.decorators import permission_decorator
from userpermissions.models import RoleModel, UserRoleModel
from masters.models import (
    Company,
    Country,
    State,
    Designation,
    Customer,
    CustomerUser,
    Drone,
    DroneAllocation,
    DashboardData,
    Plan,
    DmsSetting
    )
from masters.form import SaveCustomer, SaveCustomerUser, FrmResetPassword, UpdateCustomer
from utils.encryption import aes

encry = aes(settings.KEY, settings.IV)
ROOT_DIR = os.path.abspath(os.curdir)

BASE_URL = settings.BASE_URL
APP_NAME = settings.APP_NAME
DMS_URL = settings.DMS_URL
TABLE_ROW_LIMIT = settings.TABLE_ROW_LIMIT
EMAIL_EXPIRED_AFTER_HOUR = settings.EMAIL_EXPIRED_AFTER_HOUR
class SuccessPage(View): # pylint: disable=too-few-public-methods
    """Success Page"""
    def get(self, request):
        """Success Page Get"""
        email_varify = DmsSetting.objects.filter(conf_key='email_verification_admin').values('conf_value')
        return render(request, 'customers/success-page.html',{'dms_url':DMS_URL,'email_varify':email_varify[0]['conf_value']})
class MasterCustomersSave(View): # pylint: disable=too-few-public-methods
    """Master Customers Save"""
    def get(self, request,cid):
        """Master Customers Save Get"""
        try:
            customer_id = cid.replace("$$$", "/")
            customer_id = encry.decrypt(customer_id)
            # customer_check = CustomerUser.objects.filter(customer_id = Customer.objects.filter(customer_id=customer_id).first().id)
            customer_check = Customer.objects.filter(customer_id=customer_id).count()
            if customer_check:
                msg = "Customer Admin already created!"
                return render(request, 'customers/customer-error.html',{"msg":msg,'exist':True,'email_varify':False,'dms_url':DMS_URL})
            return render(request, 'customers/customer-add.html',{'customer_id':customer_id})
        except: # pylint: disable=W0702
            msg =  "Something went wrong!! Please contact administartor at goc@actionfi.com"
            return render(request, 'customers/customer-error.html',{"msg":msg})
class EmailVarificaion(View): # pylint: disable=too-few-public-methods
    """Email Varificaion"""
    def get(self, request,cid,date_expiry):
        """Email Varificaion Get"""
        try:
            dt_expiry = date_expiry.replace("$$$", "/")
            dt_expiry = encry.decrypt(dt_expiry)
            date_start = dt_expiry
            date_end = str(datetime.datetime.now())
            date_format_str = '%Y-%m-%d %H:%M:%S.%f'

            start = datetime.datetime.strptime(date_start, date_format_str)
            end =   datetime.datetime.strptime(date_end, date_format_str)
            diff = end - start
            ex = int(EMAIL_EXPIRED_AFTER_HOUR)*60
            diff_in_minutes = diff.total_seconds() / 60/ex
            if int(diff_in_minutes)>=1:
                msg =  "Your activation link has errorxpired"
                return render(request, 'customers/activation-error.html',{"msg":msg})
            customer_id = cid.replace("$$$", "/")
            customer_id = encry.decrypt(customer_id)
            cust = CustomerUser.objects.get(id=customer_id)
            cust.status = True
            cust.save()
            user = User.objects.get(id=CustomerUser.objects.filter(id=customer_id).first().user.id)
            user.is_active = True
            user.save()
            return render(request, 'customers/verify-success-page.html',{'dms_url':DMS_URL,'email_varify':True})
        except: # pylint: disable=W0702
            msg =  "Something went wrong!! Please contact administartor at goc@actionfi.com"
            return render(request, 'customers/customer-error.html',{"msg":msg,'email_varify':True})

class ResetPassword(View): # pylint: disable=too-few-public-methods
    """Reset Password"""
    def get(self, request,cid,date_expiry):
        """Reset Password Get"""
        try:
            dt_expiry = date_expiry.replace("$$$", "/")
            dt_expiry = encry.decrypt(dt_expiry)
            date_start = dt_expiry
            date_end = str(datetime.datetime.now())
            date_format_str = '%Y-%m-%d %H:%M:%S.%f'
            start = datetime.datetime.strptime(date_start, date_format_str)
            end =   datetime.datetime.strptime(date_end, date_format_str)
            diff = end - start
            ex = int(EMAIL_EXPIRED_AFTER_HOUR)*60
            diff_in_minutes = diff.total_seconds() / 60/ex
            if int(diff_in_minutes)>=1:
                msg =  "Your password reset link has errorxpired"
                return render(request, 'customers/password-error.html',{"msg":msg})
            email = cid.replace("$$$", "/")
            email = encry.decrypt(email)
            user = User.objects.filter(email=email).values('id')
            return render(request, 'customers/password_reset.html',{'user_id':user[0]['id']})
        except: # pylint: disable=W0702
            msg =  "Something went wrong!! Please contact administartor at goc@actionfi.com"
            return render(request, 'customers/customer-error.html',{"msg":msg})

class SaveNewPassword(View): # pylint: disable=too-few-public-methods
    """Save New Password"""
    def post(self, request):
        """Save New Password Post"""
        try:
            form = FrmResetPassword(request.POST)
            if form.is_valid():
                password = request.POST['password']
                confirm_password = request.POST['confirm_password']
                user_id = request.POST['hd_cid']
                if password != confirm_password:
                    return JsonResponse({'success': 'exist', 'msg': 'Sorry! Password not matched.'})
                user_data = User.objects.get(id=user_id)
                user_data.set_password(password)
                user_data.save()
                return JsonResponse({'success': True, 'msg': 'Password successfully changed'}, status=200)
            return JsonResponse({'success': False, 'errors': form.errors}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=500)

class PassSuccessPage(View): # pylint: disable=too-few-public-methods
    """Pass Success Page"""
    def get(self, request):
        """Pass Success Page Get"""
        return render(request, 'customers/password-success-page.html',{'dms_url':DMS_URL,'email_varify':False})

class MasterCustomersUserSave(View): # pylint: disable=too-few-public-methods
    """Master Customers User Save"""
    def post(self, request):
        """Master Customers User Save Post"""
        try:
            form = SaveCustomerUser(request.POST)
            if form.is_valid():
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                email = request.POST['email']
                phone = request.POST['phone']
                password = request.POST['password']
                confirm_password = request.POST['confirm_password']
                customer_id = request.POST['hd_cid']
                if password != confirm_password:
                    return JsonResponse({'success': 'exist', 'msg': 'Sorry! Password not matched.'})
                # email_check = CustomerUser.objects.filter(email=email).count()
                # if email_check:
                #     return JsonResponse({'success': 'exist', 'msg': 'Sorry! email already exist.'})
                cust_id = Customer.objects.get(customer_id=customer_id)
                user_data = User(
                    first_name=first_name,
                    last_name=last_name,
                    username=email,
                    email=email,
                    is_superuser=False,
                    is_staff=False,
                    is_active=False,
                    date_joined=datetime.datetime.now()
                )
                user_data.set_password(password)
                user_data.save()
                user_id = User.objects.latest('id')
                customer_user = CustomerUser(
                    first_name=first_name,
                    last_name = last_name,
                    email = email,
                    phone = phone,
                    status = False,
                    user=user_data,
                    customer = cust_id
                )
                customer_user.save()
                cust_user = CustomerUser.objects.latest('id')
                encrypt_data = encry.encrypt(str(cust_user.id))
                encrypt_data = encrypt_data.replace("/", "$$$")
                email_verification =list(DmsSetting.objects.filter(conf_key='email_verification_admin').values_list('conf_value', flat = True))
                if email_verification[0] == 'True':
                    today  = datetime.datetime.now()
                    encrypt_t = encry.encrypt(str(today))
                    encrypt_t = encrypt_t.replace("/", "$$$")
                    subject = "Email Verification"
                    end_url = f"{BASE_URL}/masters/verify_email/"+encrypt_data+"/"+encrypt_t+"/"
                    html_message = loader.render_to_string('etl/email/email_varification_template.html',
                                                        {'app_name': APP_NAME, 'name': first_name,'first_name':email,'password':'','end_url':end_url,'BASE_URL':BASE_URL})
                    send_mail(subject, '', APP_NAME + ' <do_not_reply@domain.com>', [
                    email], fail_silently=False, html_message=html_message)
                else:
                    customer_user = CustomerUser.objects.get(id=cust_user.id)
                    customer_user.status = True
                    customer_user.save()
                    user = User.objects.get(id=user_id.id)
                    user.is_active = True
                    user.save()
                role_data = RoleModel.objects.get(name='Customer Admin')
                user_role = UserRoleModel()
                user_role.role_id = role_data
                user_role.user_id = user_data
                user_role.save()
                if os.path.exists(ROOT_DIR + "/customer_list") is False:
                    os.mkdir(ROOT_DIR + "/customer_list")
                with open(ROOT_DIR + "/customer_list/"+first_name+".txt", encoding="utf-8") as file:
                    file.write("Username : "+email+" \nPassword : "+password)

                return JsonResponse({'success': True, 'msg': 'Successfully Added','password':password}, status=200)
            return JsonResponse({'success': False, 'errors': form.errors}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=500)


class MasterCustomers(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Master Customers"""
    @method_decorator(permission_decorator(permission='customer-list'))
    def get(self, request):
        """Master Customers Get"""
        query_url = ''
        # customers = Customer.objects.filter().order_by('-id')
        try:
            query = request.GET['search']
        except: # pylint: disable=W0702
            query = ''
        if query:
            customerdata = Customer.objects.filter(
                Q(account_name__icontains=request.GET['search']) |
                Q(email__icontains=request.GET["search"]) |
                Q(phone__icontains=request.GET["search"])
                ).order_by('-id')
        else:
            customerdata = Customer.objects.all().order_by('-id')
        page = request.GET.get('page', 1)
        paginator = Paginator(customerdata, TABLE_ROW_LIMIT)
        try:
            customers = paginator.page(page)
        except PageNotAnInteger:
            customers = paginator.page(1)
        except EmptyPage:
            customers = paginator.page(paginator.num_pages)
        if query:
            query_url = '&search='+query
        return render(request, 'customers/list.html', {'data': customerdata, 'customers': customers, 'query': query, 'query_url':query_url,'msg':'','groups':''})

def dictfetchall(cursor):
    """dict fetch all"""
    # "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

class GetDroneList(LoginRequiredMixin, View):# pylint: disable=too-few-public-methods
    """Get Drone List"""
    def post(self,request):
        """Get Drone List Post"""
        cid = request.POST.get('id', False)
        print(cid)
        drones = list(
            Drone.objects.filter(
                Q(allocated=False) |
                Q(id__in=DroneAllocation.objects.filter(customer=cid).values('drone_id')) &
                Q(status=True) & Q(active=True)).
                values('model','model_no','serial_no','uin','drone_type__name','id','allocated'))
        return JsonResponse({'success': True, 'data': drones}, status=200)
class MasterCustomersEdit(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Master Customers Edit"""
    @method_decorator(permission_decorator(permission='customer-edit'))
    def get(self, request,cid):
        """Master Customers Edit Get"""
        company = Company.objects.all()
        country = Country.objects.all()
        designation = Designation.objects.all()
        # drones = Drone.objects.all()
        drones = Drone.objects.filter(Q(allocated=False) | Q(id__in=DroneAllocation.objects.filter(customer=cid).values('drone')) & Q(status=True) & Q(active=True))
        drones1 = list(Drone.objects.filter(Q(allocated=False) | Q(id__in=DroneAllocation.objects.filter(customer=cid).values('drone')) & Q(status=True) & Q(active=True)).values('model','model_no','serial_no','uin','drone_type__name','id'))
        # print(serializers.serialize('json', drones1))
        cust_drones= []
        c_drones = list(DroneAllocation.objects.filter(customer=cid).values('drone'))
        for drone in c_drones:
            cust_drones.append(drone['drone'])
        customer = Customer.objects.get(id=cid)
        return render(request, 'customers/edit.html', {'cust_drones':cust_drones,'drones':drones,'drones1':drones1,'customer':customer,'company': company, 'country': country, 'designation': designation})

    @method_decorator(permission_decorator(permission='customer-update'))
    def post(self,request,cid): #pylint: disable=R0915
        """Master Customers Edit Post"""
        try:
            form = UpdateCustomer(cid,request.POST)
            if form.is_valid():
                first_name = request.POST['first_name']
                email = request.POST['email']
                phone = request.POST['phone']
                activation_date = datetime.datetime.strptime(str(request.POST['activation_date']), '%Y-%m-%d')
                address = request.POST['address']
                country = Country.objects.get(id=int(request.POST['country']))
                state = State.objects.get(id=int(request.POST['state']))
                description = request.POST['description']
                active = request.POST['active']
                # email_check = Customer.objects.filter(email=email).exclude(id=cid).count()
                # if email_check:
                #     return JsonResponse({'success': 'exist', 'msg': 'Sorry! email already exist.'})
                customer_data = Customer.objects.get(id=cid)
                customer_data.account_name=first_name
                customer_data.email = email
                customer_data.phone = phone
                customer_data.activation_date = activation_date
                customer_data.address =  address
                customer_data.country = country
                customer_data.state = state
                customer_data.description = description
                customer_data.status = active
                customer_data.user=request.user
                customer_data.save()
                drone_a = Drone.objects.filter(Q(allocated=False) | Q(id__in=DroneAllocation.objects.filter(customer=cid).values('drone')))
                for drone in drone_a:
                    Drone.objects.filter(id = drone.id).update(allocated=False)
                DroneAllocation.objects.filter(customer=cid).delete()
                selected = request.POST.getlist('selected[]')
                for drone_id in selected:
                    Drone.objects.filter(id = drone_id).update(allocated=True)
                    drone = Drone.objects.get(id=drone_id)
                    drone_allocation = DroneAllocation(
                        drone=drone,
                        customer=customer_data
                    )
                    drone_allocation.save()
                    customer_id = Customer.objects.filter(id=cid).values('id')
                    dashboard_data = DashboardData.objects.filter(drone = drone_id,customer_id=cid).values('distance','flying_time','plans','id')
                    plans = Plan.objects.filter(drone=drone_id,customer_id=cid)
                    if dashboard_data.count() == 0:
                        dashboard_data = DashboardData(
                            plans = plans.count(),
                            gc_con_status = False,
                            status = True,
                            drone = drone,
                            customer_id = customer_id
                        )
                        dashboard_data.save()
                    dashboard_data = DashboardData.objects.filter(drone = drone_id,customer_id=cid).values('distance','flying_time','plans','id')
                    plans = Plan.objects.filter(drone=drone_id,customer=cid)
                    if dashboard_data.count() > 0:
                        dashboard_data = DashboardData.objects.get(id = dashboard_data[0]['id'])
                        dashboard_data.plans = plans.count()
                        dashboard_data.save()
                    else:
                        dashboard_data = DashboardData(
                            # distance = flight_distance,
                            # flying_time = new_t,
                            plans = plans.count(),
                            gc_con_status = False,
                            status = False,
                            drone = drone,
                            customer_id = customer_id
                        )
                        dashboard_data.save()
                return JsonResponse({'success': True, 'msg': 'Successfully Updated'}, status=200)
            return JsonResponse({'success': False, 'errors': form.errors}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=500)
class MasterCustomersAdd(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Master Customers Add """
    @method_decorator(permission_decorator(permission='customer-add'))
    def get(self, request):
        """Master Customers Add Get"""
        company = Company.objects.all()
        country = Country.objects.all()
        designation = Designation.objects.all()
        return render(request, 'customers/add.html', {'company': company, 'country': country, 'designation': designation})
    @method_decorator(permission_decorator(permission='customer-save'))
    def post(self, request):
        """Master Customers Add Post"""
        try:
            form = SaveCustomer(request.POST)
            if form.is_valid():
                first_name = request.POST['first_name']
                email = request.POST['email']
                phone = request.POST['phone']
                activation_date = datetime.datetime.strptime(str(request.POST['activation_date']), '%Y-%m-%d')
                address = request.POST['address']
                country = Country.objects.get(id=int(request.POST['country']))
                state = State.objects.get(id=int(request.POST['state']))
                description = request.POST['description']
                active = request.POST['active']
                # email_check = Customer.objects.filter(email=email).count()
                # if email_check:
                #     return JsonResponse({'success': 'exist', 'msg': 'Sorry! email already exist.'})
                customer = Customer(
                    account_name=first_name,
                    email = email,
                    phone = phone,
                    activation_date = activation_date,
                    address =  address,
                    country = country,
                    state = state,
                    description = description,
                    status = active,
                    user=request.user,
                )
                customer.save()
                return JsonResponse({'success': True, 'msg': 'Successfully Added'}, status=200)
            return JsonResponse({'success': False, 'errors': form.errors}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=500)

class GetState(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Get State"""
    def post(self, request):
        """Get State Post"""
        try:
            json_data = request.body.decode("utf-8")
            data = json.loads(json_data)
            state =''
            if data['id']:
                state = serializers.serialize('json', State.objects.filter(country=data['id']))
            return JsonResponse({'success': True, 'data': state}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=500)
