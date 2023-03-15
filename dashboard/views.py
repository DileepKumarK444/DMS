from django.http import *
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
import datetime
from django.db.models import Q
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from django.utils.decorators import method_decorator
from masters.decorators import permission_decorator
# def dashboard(request):
#     return render(request, 'dashboard/dashboard.html')
	# logout(request)
	# username = password = ''
	# if request.POST:
	# 	username = request.POST['username']
	# 	password = request.POST['password']
	# 	user = authenticate(username=username, password=password)
	# 	if user is not None:
	# 		if user.is_active:
	# 			login(request, user)
	# 			return HttpResponseRedirect('/dms/masters/battery/')
	# 	else:
	# 		return render(request, 'etl/login.html',{ 'err_msg' :'Invalid credentials'})
	# 		#return render_to_response('etl/login.html', context_instance=RequestContext(request))
	# else:
	# 	return render(request, 'etl/login.html')

class Dashboard(LoginRequiredMixin, View):
	@method_decorator(permission_decorator(permission='dashboard-view'))
	def get(self, request):
		print(request)
		log_count=10
		return render(request, 'dashboard/dashboard.html',{'log_count':log_count})