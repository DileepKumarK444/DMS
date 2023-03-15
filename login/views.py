from django.http import *
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
import datetime
from django.views import View
from django.db.models import Q
from utils import helper
from django.core.mail import send_mail
from django.template import loader
from dms.settings import APP_NAME, BASE_URL
from django.contrib.auth.models import User
from django.conf import settings
from utils.encryption import aes
import os

from login.form import FrmResetPassword

encry = aes(settings.KEY, settings.IV)
ROOT_DIR = os.path.abspath(os.curdir)
BASE_URL = settings.BASE_URL
APP_NAME = settings.APP_NAME
EMAIL_EXPIRED_AFTER_HOUR = settings.EMAIL_EXPIRED_AFTER_HOUR
# def login_user(request):
# 	logout(request)
# 	username = password = ''
# 	if request.POST:
# 		username = request.POST['username']
# 		password = request.POST['password']
# 		user = authenticate(username=username, password=password)
# 		if user is not None:
# 			if user.is_active:
# 				login(request, user)
# 				return HttpResponseRedirect('/dashboard/')
# 		else:
# 			return render(request, 'etl/login.html',{ 'err_msg' :'Invalid credentials'})
# 			#return render_to_response('etl/login.html', context_instance=RequestContext(request))
# 	else:
# 		return render(request, 'etl/login.html')

class CheckLogin(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/dashboard/')
        else:
            return render(request, 'login/login.html')

    def post(self, request):
        logout(request)
        username = password = ''
        if request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # return HttpResponseRedirect('/dashboard/')
                    if not request.user.is_superuser:
                        # Store Permissions in session
                        allowed_permissions = helper.get_all_user_permissions(
                            request.user.id)
                        request.session['permissions'] = allowed_permissions
                    request.test = 10
                    
                    return HttpResponseRedirect('/dashboard/')
            else:
                return render(request, 'login/login.html', {'err_msg': 'Invalid credentials'})
class Logout(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/auth/login/')

class ForgotPassword(View):
    def get(self,request):
        return render(request, 'login/forgot_password.html')

    def post(self,request):
        email = request.POST['email']
    
        email_exist = User.objects.filter(email=email).values('first_name')
        if(email_exist.count()<=0):
            # return Response({'msg':'Email does not exist!','st':False})
            return render(request, 'login/forgot_password.html', {'msg': 'Email does not exist!','status':False})
        encryptData = encry.encrypt(str(email))
        encryptData = encryptData.replace("/", "$$$")

        t  = datetime.datetime.now()

        encrypt_t = encry.encrypt(str(t))
        encrypt_t = encrypt_t.replace("/", "$$$")

        subject = "Password Reset"
        end_url = f"{BASE_URL}/auth/reset_password/"+encryptData+"/"+encrypt_t+"/"
        # html_message = loader.render_to_string('etl/email/forgot_password.html',
        #                                        {'app_name': APP_NAME, 'name': name, 'username': username,
        #                                         'password': password, 'login_url': BASE_URL})

        # send_mail('User Account Created', '', APP_NAME + ' <do_not_reply@domain.com>', [
        #     email], fail_silently=False, html_message=html_message)
        html_message = loader.render_to_string('etl/email/forgot_password.html',
                                        {'app_name': APP_NAME, 'name': email_exist[0]['first_name'],'email':email,'end_url':end_url,'EMAIL_EXPIRED_AFTER_HOUR':EMAIL_EXPIRED_AFTER_HOUR,'BASE_URL':BASE_URL})
        send_mail(subject, '', APP_NAME + ' <do_not_reply@domain.com>', [
        email], fail_silently=False, html_message=html_message)

        return render(request, 'login/forgot_password.html', {'msg': 'Password reset link has been sent to your email!','status':True})

class ResetPassword(View):
    def get(self, request,cid,t):
        try:
            tm = t.replace("$$$", "/")
            tm = encry.decrypt(tm)
            date_1 = tm
            date_2 = str(datetime.datetime.now())
            date_format_str = '%Y-%m-%d %H:%M:%S.%f'

            start = datetime.datetime.strptime(date_1, date_format_str)
            end =   datetime.datetime.strptime(date_2, date_format_str)
            diff = end - start
            ex = int(EMAIL_EXPIRED_AFTER_HOUR)*60
            diff_in_minutes = diff.total_seconds() / 60/ex
            if(int(diff_in_minutes)>=1):
                msg =  "Your password reset link has expired"
                return render(request, 'customers/password-error.html',{"msg":msg}) 

            email = cid.replace("$$$", "/")
            email = encry.decrypt(email)
            # email_check = CustomerUser.objects.filter(email = email)
            user = User.objects.filter(email=email).values('id')
            # if email_check:
            #     msg = "Customer Admin already created!"
            #     return render(request, 'customers/customer-error.html',{"msg":msg,'exist':True,'email_varify':False})
            # else:
            return render(request, 'login/password_reset.html',{'user_id':user[0]['id']})
        except Exception as e :
                msg =  "Something went wrong!! Please contact administartor at goc@actionfi.com"
                return render(request, 'customers/customer-error.html',{"msg":e})  
class SaveNewPassword(View):
    def post(self,request):
        try:
            print('form.is_valid()')
            form = FrmResetPassword(request.POST)
            
            if form.is_valid():
                password = request.POST['password']
                confirm_password = request.POST['confirm_password']
                user_id = request.POST['hd_cid']
                
                if (password != confirm_password):
                    return JsonResponse({'success': 'exist', 'msg': 'Sorry! Password not matched.'})
                
                user_data = User.objects.get(id=user_id)
                user_data.set_password(password)
                user_data.save()
                
                return JsonResponse({'success': True, 'msg': 'Password successfully changed'}, status=200)
            else:
                return JsonResponse({'success': False, 'errors': form.errors}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'msg': str(e)}, status=500)