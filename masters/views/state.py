# pylint: disable=no-member
"""
State Master
"""
# pylint: disable=E0401
import os

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from django.views import View
from django.conf import settings

from masters.models import Country, State,Customer
from masters.form import SaveState,UpdateState

from userpermissions.decorators import permission_decorator

from utils.encryption import aes
encry = aes(settings.KEY, settings.IV)
ROOT_DIR = os.path.abspath(os.curdir)

BASE_URL = settings.BASE_URL
APP_NAME = settings.APP_NAME
DMS_URL = settings.DMS_URL
TABLE_ROW_LIMIT = settings.TABLE_ROW_LIMIT

class StateList(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """State List"""
    @method_decorator(permission_decorator(permission='state-list'))
    def get(self, request):
        """State List Get"""
        query_url = ''
        # state = State.objects.filter().order_by('-id')
        try:
            query = request.GET['search']
        except: # pylint: disable=W0702
            query = ''
        if query:
            statedata = State.objects.filter(
                Q(name__icontains=request.GET['search']) |
                Q(description__icontains=request.GET["search"]) |
                Q(country__name__icontains=request.GET["search"])
                ).order_by('-id')
        else:
            statedata = State.objects.all().order_by('-id')
        page = request.GET.get('page', 1)
        paginator = Paginator(statedata, TABLE_ROW_LIMIT)
        try:
            state = paginator.page(page)
        except PageNotAnInteger:
            state = paginator.page(1)
        except EmptyPage:
            state = paginator.page(paginator.num_pages)
        if query:
            query_url = '&search='+query
        country = Country.objects.all()
        return render(request, 'state/list.html', {'data': statedata, 'query': query, 'state': state,'query_url':query_url, 'country':country,'msg':''})

    @method_decorator(permission_decorator(permission='state-delete'))
    def delete(self, request):
        """State List Delete"""
        try:
            state_check = Customer.objects.filter(state=request.GET['id']).count()
            if state_check:
                return JsonResponse({'success': 'exist', 'msg': 'Sorry can\'t delete, State already have transaction.'})
            data = State.objects.get(id=request.GET['id'])
            data.delete()
            return JsonResponse({'success': True, 'url': '/masters/state/'}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=500)
class StateAdd(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """State Add"""
    @method_decorator(permission_decorator(permission='state-save'))
    def post(self, request):
        """State Add Post"""
        try:
            form = SaveState(request.POST)
            if form.is_valid():
                name = request.POST['txt_name']
                description = request.POST['description']
                # type_check = State.objects.filter(name=name, country=request.POST['country']).count()
                # if type_check:
                #     return JsonResponse({'success': 'exist', 'msg': 'Sorry! State already exist.'})
                country = Country.objects.get(id = request.POST['country'])
                state = State(
                    name=name,
                    description = description,
                    user = request.user,
                    country = country
                )
                state.save()
                return JsonResponse({'success': True, 'msg': 'Successfully Added'}, status=200)
            return JsonResponse({'success': False, 'errors': form.errors}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=500)

class StateUpdate(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """State Update"""
    @method_decorator(permission_decorator(permission='state-update'))
    def post(self, request):
        """State Update Post"""
        try:
            form = UpdateState(request.POST)
            if form.is_valid():
                name = request.POST['txt_name']
                description = request.POST['description']
                state_id = request.POST['typeid']
                # type_check = State.objects.filter(name=name, country = request.POST['country']).exclude(id=state_id).count()
                # if type_check:
                #     return JsonResponse({'success': 'exist', 'msg': 'Sorry! State already exist.'})
                country = Country.objects.get(id = request.POST['country'])
                state = State.objects.get(id=state_id)
                state.name = name
                state.description = description
                state.country = country
                state.save()
                return JsonResponse({'success': True, 'msg': 'Successfully Updated'}, status=200)
            return JsonResponse({'success': False, 'errors': form.errors}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=500)
