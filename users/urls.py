from django.urls import path
from users.views import users

urlpatterns = [

    # USER
     path('list/', users.MasterUser.as_view(),
         name='User List'),
     path('edit/', users.MasterUserEdit.as_view(),
         name='Update User'),
     path('redirect/', users.RedirectUser.as_view(),
         name='Redirect User'),
]
