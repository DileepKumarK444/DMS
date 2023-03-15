from django.urls import path
from . import views

urlpatterns = [
	# path('login/',views.login_user, name='login_user'),
	# path('',views.dashboard, name='dashboard'),
	path('', views.Dashboard.as_view(), name='Dashboard view'),
	
]