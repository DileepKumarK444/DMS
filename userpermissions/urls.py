from django.urls import path
from userpermissions.views import permission, roles, group, permission_group

urlpatterns = [
    path('roles/', roles.MasterRoles.as_view(),
         name='Manage Roles'),
    path('roles-update/', roles.MasterUpdateRoles.as_view(),
         name='Manage Roles'),

    path('group/', group.MasterGroup.as_view(),
         name='Manage Group'),
    path('group-update/', group.MasterUpdateGroup.as_view(),
         name='Manage Group'),

    path('manage/', permission.MasterPermission.as_view(),
         name='Manage Permission'),
    path('manage/update/', permission.MasterUpdatePermission.as_view(),
         name='Manage Permission'),

    path('permission-group/', permission_group.MasterPermission.as_view(),
         name='Manage Permission Group relation'),
]
