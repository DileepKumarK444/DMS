# pylint: disable=no-member
"""
Country Master
"""

import os
# pylint: disable=E0401
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.conf import settings
from utils.encryption import aes
from masters.models import Country, State
from masters.form import SaveCountry, UpateCountry
from userpermissions.decorators import permission_decorator
# pylint: disable=E0401

encry = aes(settings.KEY, settings.IV)
ROOT_DIR = os.path.abspath(os.curdir)

BASE_URL = settings.BASE_URL
APP_NAME = settings.APP_NAME
DMS_URL = settings.DMS_URL
TABLE_ROW_LIMIT = settings.TABLE_ROW_LIMIT

class CountryList(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Country List and Delete"""
    @method_decorator(permission_decorator(permission='country-list'))
    def get(self, request):
        """Country List view"""
        # country = Country.objects.filter().order_by('-id')
        query_url = ''
        try:
            query = request.GET.get('search') or ''
        except TypeError:
            query = ''
        if query:
            countrydata = Country.objects.filter(
                Q(name__icontains=request.GET.get('search')) |
                Q(description__icontains=request.GET.get('search'))).order_by('-id')
        else:
            countrydata = Country.objects.all().order_by('-id')

        page = request.GET.get('page', 1)
        paginator = Paginator(countrydata, int(TABLE_ROW_LIMIT))

        try:
            country = paginator.page(page)
        except PageNotAnInteger:
            country = paginator.page(1)
        except EmptyPage:
            country = paginator.page(paginator.num_pages)
        if query:
            query_url = '&search='+query
        return render(request, 'country/list.html', {
                'data': countrydata,
                'query': query,
                'country': country,
                'query_url':query_url,
                'msg':''
            })
    @method_decorator(permission_decorator(permission='country-delete'))
    def delete(self, request):
        """Country Delete"""
        try:
            state_check = State.objects.filter(country=request.GET['id']).count()
            if state_check:
                return JsonResponse({
                    'success': 'exist',
                    'msg': 'Sorry can\'t delete, Country already have transaction.'
                    }, status=401)
            data = Country.objects.get(id=request.GET['id'])
            data.delete()
            return JsonResponse({'success': True, 'url': '/masters/country/'}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=200)
class CountryAdd(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Country Save"""
    @method_decorator(permission_decorator(permission='country-save'))
    def post(self, request):
        """Country save post"""
        try:
            form = SaveCountry(request.POST)
            if form.is_valid():
                name = request.POST['txt_name']
                description = request.POST['description']
                # type_check = Country.objects.filter(name=name).count()
                # if type_check:
                #     return JsonResponse({
                #         'success': 'exist',
                #         'msg': 'Sorry! Country already exist.'
                #         }, status=401)
                country = Country(
                name=name,
                description = description,
                user = request.user
                )
                country.save()
                return JsonResponse({'success': True, 'msg': 'Successfully Added'}, status=200)
            return JsonResponse({'success': False, 'errors': form.errors}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=500)
class CountryUpdate(LoginRequiredMixin, View): # pylint: disable=too-few-public-methods
    """Country Update"""
    @method_decorator(permission_decorator(permission='country-update'))
    def post(self, request):
        """Country update post"""
        try:
            form = UpateCountry(request.POST)
            if form.is_valid():
                name = request.POST['txt_name']
                description = request.POST['description']
                _id = request.POST['typeid']
                # type_check = Country.objects.filter(name=name).exclude(id=_id).count()
                # if type_check:
                #     return JsonResponse({
                #         'success': 'exist',
                #         'msg': 'Sorry! Country already exist.'
                #         })
                country = Country.objects.get(id=_id)
                country.name = name
                country.description = description
                country.save()
                return JsonResponse({'success': True, 'msg': 'Successfully Updated'}, status=200)
            return JsonResponse({'success': False, 'errors': form.errors}, status=200)
        except Exception as error: # pylint: disable=W0703
            return JsonResponse({'success': False, 'msg': str(error)}, status=500)
