from django.urls import path
from .views import SystemSettingsUpdateView

app_name = 'core'

urlpatterns = [
    path('admin/system-settings/', SystemSettingsUpdateView.as_view(), name='system_settings'),
]
