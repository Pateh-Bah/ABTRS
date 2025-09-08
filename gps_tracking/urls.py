from django.urls import path
from . import views

app_name = "gps_tracking"

urlpatterns = [
    # Public views
    path("", views.BusTrackingMapView.as_view(), name="public_map"),
    path("bus/<int:pk>/", views.BusDetailView.as_view(), name="bus_detail"),
    
    # Admin views
    path("admin/", views.AdminGPSManagementView.as_view(), name="admin_dashboard"),
    path("admin/buses/", views.AdminBusLocationListView.as_view(), name="admin_bus_list"),
    path("admin/speed-alerts/", views.SpeedAlertListView.as_view(), name="admin_speed_alerts"),
    path("admin/emergency-alerts/", views.EmergencyAlertListView.as_view(), name="admin_emergency_alerts"),
    
    # Driver views
    path("driver/", views.DriverDashboardView.as_view(), name="driver_dashboard"),
    path("driver/tracking/", views.driver_tracking, name="driver_tracking"),
    
    # API endpoints
    path("api/bus/<int:pk>/update-location/", views.UpdateBusLocationAPIView.as_view(), name="api_update_location"),
    path("api/driver/update-location/", views.DriverLocationUpdateAPIView.as_view(), name="api_driver_update_location"),
    path("api/buses/locations/", views.GetBusLocationsAPIView.as_view(), name="api_bus_locations"),
    path("api/passenger/buses/", views.PassengerBusTrackingAPIView.as_view(), name="api_passenger_buses"),
    path("api/bus/<int:pk>/progress/", views.RouteProgressAPIView.as_view(), name="api_route_progress"),
    path("api/bus/<int:pk>/emergency/", views.TriggerEmergencyAlertAPIView.as_view(), name="api_emergency_alert"),
    
    # Actions
    path("admin/speed-alert/<int:pk>/acknowledge/", views.AcknowledgeSpeedAlertView.as_view(), name="acknowledge_speed_alert"),
    path("admin/emergency-alert/<int:pk>/resolve/", views.ResolveEmergencyAlertView.as_view(), name="resolve_emergency_alert"),
]