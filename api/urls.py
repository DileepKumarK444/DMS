from django.urls import path
from api.views import user_api, customers_api, project_api, pilot_api, plan_api, api

urlpatterns = [
	path("login/",
          user_api.login_check, name = 'login_check'),
      path('role_permissions/', user_api.UserRolePermissions,
         name='user-role-permissions'),

      path('get_customer_details/', customers_api.UserCustomerDetails,
         name='get-customer-details'),
      path('save_user_details/', customers_api.UserCustomerSave,
         name='save-user-details'),
      path('get_user_list/', customers_api.GetUserList,
         name='get_user_list'),
      path('save_customer/', customers_api.CustomerSave,
         name='save_customer'),

      path('add_project/', project_api.AddProject,
         name='add_project'),
      path('get_project_list/', project_api.GetProjectList,
         name='get_project_list'),

      # path('add_pilot/', pilot_api.AddPilot,
      #    name='add_pilot'),
      # path('get_pilot_list/', pilot_api.GetPilotList,
      #    name='get_pilot_list'),

      # path('save_plan_details/', plan_api.AddPlan,
      #    name='save_plan_list'),
      path('save_plan/', plan_api.SavePlan,
         name='save_plan'),
      path('update_plan/', plan_api.UpdatePlan,
         name='Update_plan'),
         
      # path('running_plan_data/', plan_api.RunningPlanData,
      #    name='running_plan_data'),
      path('get_drone_details/', api.GetDroneDetails,
         name='save_drone_list'),
      path('get_sel_user/', customers_api.GetSelectedUserDetails,
         name='get_sel_user'),
      path('update_user/', customers_api.UserCustomerUpdate,
         name='update_user'),
      path('delete_user/', customers_api.DeleteUser,
         name='delete_user'),
      path('delete_project/', project_api.DeleteProject,
         name='delete_project'),
      path('get_sel_project/', project_api.getSelectedPojectDetails,
         name='get_sel_project'),
      path('update_project/', project_api.ProjectUpdate,
         name='update_project'),

      path('get_checklist/', api.getChecklist,
         name='get_checklist'),
      path('get_drone_list/', api.getDronesList,
         name='get_drone_list'),
      path('get_drone/', api.getDrone,
         name='get_drone'),

      path('save_checklist/', api.saveChecklist,
         name='save_checklist'),

      path('save_log_data/', api.saveLogData,
         name='save_log_data'),

      path('download_log/', api.downloadLog,
         name='download_log'),

      path('get_filtered_reports/', api.getFilteredReports,
         name='get_filtered_reports'),
      
      # path('get_filtered_reports1/', api.getFilteredReports1,
      #    name='get_filtered_reports1'),

      path('get_dashboard_data/', api.getDashboardData,
         name='get_dashboard_data'),
      path('forgot_password/', api.forgotPassword,
         name='forgot_password'),
      
      path('file_upload/', api.fileUpload,
         name='file_upload'),
      path('download_licence/', api.downloadLicence,
         name='download_licence'),
      path('change_password/', api.changePassword,
         name='change_password'),
      path('get_drone_image/', api.getDroneImage,
         name='get_drone_image'),
      # path('get_login_token/', api.getLoginToken,
      #    name='get_login_token'),

      path('get_drone_log/', api.getDroneLog,
         name='get_drone_log'),

      path('list/', customers_api.ApiUserView.as_view(),
         name='list'),
      path('api_logs_view/', customers_api.ApiLogView,
         name='list'),

      path('get_profile_schema/', api.getProfileSchema,
         name='get_profile_schema'),

      path('get_plan/', api.getPlan,
         name='get_plan'), 
      path('handshake_validation/', api.HandshakeValidation,
         name='handshake_validation'),
      path('get_release_plan/', api.GetReleasePlan,
         name='get_release_plan'),

      path('project_list/', api.ProjectList,
         name='project_list'),
      path('pilot_list/', api.PilotList,
         name='pilot_list'),
      path('read_data/', api.ReadData,
         name='read_data'),
      
      path('update_fields/', api.UpdateSubsetFields,
         name='update_fields'),
      
      path('consumption_log/', api.SaveConsumptionLog,
         name='consumption_log')

      

         
         

      

         
      

      

         

         

         
      

      
	
]