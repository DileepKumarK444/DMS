
from django.http import *
from rest_framework.authtoken.models import Token
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.db.models import Q
import json
from django.template import loader
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from masters.decorators import permission_decorator
from users.form import SaveUserForm, EditUserForm
from django.contrib.auth.hashers import make_password
from masters.models import Profile
from datetime import datetime
from dms.settings import APP_NAME, BASE_URL
from userpermissions.models import RoleModel, UserRoleModel
import pytz
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
import os
from utils.encryption import aes
from django.conf import settings

TABLE_ROW_LIMIT = settings.TABLE_ROW_LIMIT
# from django.template import loader

# from django.db import connection
ROOT_DIR = os.path.abspath(os.curdir)

encry = aes(settings.KEY, settings.IV)

class MasterUser(LoginRequiredMixin, View):

    # USER LISTING PAGE
    @method_decorator(permission_decorator(permission='user-menu'))
    def get(self, request):
        query_url = ''
        try:
            query = request.GET['search']
        except Exception as e:
            query = ''
        if query:
            userdata = User.objects.filter(
                Q(first_name__icontains=request.GET['search']) | Q(email__icontains=request.GET['search']) | Q(username__icontains=request.GET['search']) | Q(last_login__icontains=request.GET['search']) | Q(date_joined__icontains=request.GET['search']) & Q(is_superuser=False)).order_by('-date_joined')
                
        else:
            userdata = User.objects.filter(
                Q(is_superuser=False)).order_by('-date_joined')
        page = request.GET.get('page', 1)
        paginator = Paginator(userdata, TABLE_ROW_LIMIT)

        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        roles = RoleModel.objects.all()
        profiles = Profile.objects.all()
        if query:
                query_url = '&search='+query
        timeZone_datas = [{'text': tzone, 'offset': datetime.now(pytz.timezone(tzone)).strftime('%z')} for tzone in pytz.all_timezones]
        return render(request, 'user/manage.html', {'data': userdata, 'users': users, 'query': query, 'roles': roles,'query_url':query_url,'timeZone_datas':timeZone_datas,'profiles':profiles,'DMS_URL':settings.DMS_URL})

    # TO ADD USER
    @method_decorator(permission_decorator(permission='add-user'))
    def post(self, request):
        try:
            form = SaveUserForm(request.POST)
            if form.is_valid():
                name = request.POST['name']
                email = request.POST['email']
                username = request.POST['username']
                password = request.POST['password']
                role = request.POST['role']
                timezone = request.POST['timezone']

                username_exist = self._check_unique(
                    "username", username, None)
                if username_exist:
                    return JsonResponse(
                        {'success': False, 'msg': 'username already exist'}, status=400)

                role_data = RoleModel.objects.get(id=role)

                user_data = User(
                    first_name=name,
                    last_name='',
                    username=username,
                    email=email,
                    password=make_password(password),
                    is_superuser=False,
                    is_staff=False,
                    is_active=True,
                    date_joined=datetime.now()
                )
                user_data.save()
                user = User.objects.latest('id')
                # print('User',user.id)
                user_role = UserRoleModel()
                user_role.role_id = role_data
                user_role.user_id = user_data
                user_role.save()

                profile = Profile.objects.filter(user_id=user.id)
                if (len(profile)):
                    profile_data = profile[0]
                else:
                    profile_data = Profile()
                    profile_data.user = user
                profile_data.time_zone = timezone
                profile_data.save()


                # Send mail to user with credentials
                self._registration_mail_to_user(
                    name, username, password, email)

                return JsonResponse({'success': True, 'msg': 'Successfully Added'}, status=200)
            else:
                return JsonResponse({'success': False, 'errors': form.errors}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'msg': str(e)}, status=500)

    # SEND USER CREDENTIALS TO MAIL
    # PRIVATE FUNCTION
    def _registration_mail_to_user(self, name, username, password, email):
        html_message = loader.render_to_string('etl/email/user_registration.html',
                                               {'app_name': APP_NAME, 'name': name, 'username': username,
                                                'password': password, 'login_url': BASE_URL,'BASE_URL':BASE_URL})

        send_mail('User Account Created', '', APP_NAME + ' <do_not_reply@domain.com>', [
            email], fail_silently=False, html_message=html_message)

    # CHECK EMAIL ID EXIST
    # PRIVATE FUNCTION
    def _check_unique(self, field_type, field_value, id):
        if field_type == "username":
            users = User.objects.filter(Q(username=field_value))

        if field_type == "email":
            users = User.objects.filter(Q(email=field_value))

        if id is not None:
            users = users.filter(
                ~Q(id=id))

        return len(users)

    # TO DELETE USER
    @method_decorator(permission_decorator(permission='delete-user'))
    def delete(self, request):
        try:
            data = User.objects.get(id=request.GET['id'])
            data.delete()
            return JsonResponse({'success': True, 'url': '/users/list/'}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'msg': str(e)}, status=200)


class MasterUserEdit(LoginRequiredMixin, View):

    # TO UPDATE USER
    @method_decorator(permission_decorator(permission='edit-user'))
    def post(self, request):
        try:
            form = EditUserForm(request.POST)
            if form.is_valid():
                name = request.POST['name']
                email = request.POST['email']
                username = request.POST['username']
                timezone = request.POST['timezone']
                role = request.POST['role']
                userid = request.POST.get(
                    'userid') and request.POST.get('userid') or None

                role_data = RoleModel.objects.get(id=role)

                master_user = MasterUser()
                username_exist = master_user._check_unique(
                    "username", username, userid)
                if username_exist:
                    return JsonResponse(
                        {'success': False, 'msg': 'username already exist'}, status=400)

                user = User.objects.get(id=userid)
                user.first_name = name
                user.email = email
                user.username = username
                user.save()
                try:
                    user_group = UserRoleModel.objects.get(
                        user_id=user)
                except:
                    user_group = UserRoleModel()
                    user_group.user_id = user
                user_group.role_id = role_data
                user_group.save()

                profile = Profile.objects.filter(user_id=userid)
                if (len(profile)):
                    profile_data = profile[0]
                else:
                    profile_data = Profile()
                    profile_data.user = user
                profile_data.time_zone = timezone
                profile_data.save()

                return JsonResponse({'success': True, 'msg': 'Successfully Updated'}, status=200)
            else:
                return JsonResponse({'success': False, 'errors': form.errors}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'msg': str(e)}, status=500)

class RedirectUser(LoginRequiredMixin, View):

    # TO UPDATE USER
    @method_decorator(permission_decorator(permission='login-avm'))
    def post(self, request):
        try:
            id = request.POST['id']
            user_check = User.objects.filter(id=request.POST['id'],is_active=False).count()
            if user_check:
                return JsonResponse({'success': 'exist', 'msg': 'Sorry this account is deactivated now.'})

            user = User.objects.get(id=id)
            token, _ = Token.objects.get_or_create(user=user)
            token = self.token_expire_handler(token)
            encryptData = encry.encrypt(str(token))
            encryptData = encryptData.replace("/", "@*@")
            encryptData = encryptData.replace("+", "$*$")
            return JsonResponse({'success': True, 'msg': '','id':encryptData}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'msg': str(e)}, status=500)
    @staticmethod
    def expires_in(token):
        time_elapsed = timezone.now() - token.created
        left_time = timedelta(
            seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
        return left_time

    def is_token_expired(self, token):
        return self.expires_in(token) < timedelta(seconds=0)

    def token_expire_handler(self, token):
        is_expired = self.is_token_expired(token)
        if is_expired:
            token.delete()
            token = Token.objects.create(user=token.user)
        return token
