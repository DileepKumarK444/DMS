from django.urls import path
from . import views

urlpatterns = [
	# path('login/',views.login_user, name='login_user'),
	# path('',views.login_user, name='login_user'),
    path('login/', views.CheckLogin.as_view(), name='Login view'),
    # path('login/', views.CheckLogin.as_view(), name='Login Post'),
    path('logout/', views.Logout.as_view(), name='Log out'),
    path('forgotpassword/', views.ForgotPassword.as_view(), name='Forgot Password'),
    path('reset_password/<str:cid>/<str:t>/', views.ResetPassword.as_view(), name='Reset Password'),
    path('save_new_password/', views.SaveNewPassword.as_view(), name='Save New Passord'),
	
]