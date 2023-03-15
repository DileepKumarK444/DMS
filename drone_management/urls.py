from django.urls import path
from drone_management.views import drones, consumption_log

urlpatterns = [
     path('drone-details/', drones.DroneList.as_view(),
          name='Drone Details List'),
     path('drone-details/add/', drones.DroneAdd.as_view(),
          name='Drone Details Add'),
     path('drone-details/getSchema/', drones.getSchema.as_view(),
          name='get Schema Details'),
     path('drone-details/edit/<int:cid>/', drones.DroneEdit.as_view(),
          name='Drone Details Edit'),
     path('drone-details/onLoad/', drones.onLoad.as_view(),
          name='get Drone Details'),
     path('drone-details/update/', drones.DroneUpdate.as_view(),
          name='Drone Details Update'),

     path('drone-details/getFeatures/', drones.getFeatures.as_view(),
          name='get-features'),
          
     # path('drone-list?d'),
     path('drone-details/get_drone_type/', drones.GetDroneType.as_view(),
          name='Get Drone Type'),
     path('drone-details/config/<int:cid>', drones.GetConfig.as_view(),
          name='Get Config'),
     path('drone-details/save_config/', drones.SaveConfig.as_view(),
          name='Save Config'),
     path('drone-details/activate/', drones.ActivateDrone.as_view(),
          name='Activate Drone'),
     path('drone-details/test_connection/', drones.TestConnection.as_view(),
          name='Test Connection'),
     
     path('consumption_log/', consumption_log.ConsumptionLogList.as_view(),
          name='consumption log list'),
     path('update_log_status/', consumption_log.UpdateLogStatus.as_view(),
          name='update log status'),
     
     # path('customers/edit/<int:cid>/', customers.MasterCustomersEdit.as_view(),
     #      name='Manage customers Edit'),

]
