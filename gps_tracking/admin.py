from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    Driver, BusLocation, SpeedAlert, RouteProgress,
    GeofenceArea, EmergencyAlert
)


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'license_number', 'phone_number', 
        'assigned_bus', 'current_speed_display', 'is_active'
    )
    list_filter = ('is_active',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'license_number', 'phone_number')
    readonly_fields = ('created_at', 'updated_at', 'current_location_display', 'current_speed_display')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'license_number', 'phone_number')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact', 'emergency_contact_phone')
        }),
        ('Assignment', {
            'fields': ('assigned_bus', 'is_active')
        }),
        ('GPS Status', {
            'fields': ('current_location_display', 'current_speed_display'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def current_speed_display(self, obj):
        speed = obj.current_speed
        if speed > 80:
            color = 'red'
        elif speed > 60:
            color = 'orange'
        else:
            color = 'green'
        return format_html(
            '<span style="color: {};">{:.1f} km/h</span>',
            color, speed
        )
    current_speed_display.short_description = 'Current Speed'
    
    def current_location_display(self, obj):
        location = obj.current_location
        if location and hasattr(location, 'latitude'):
            return format_html(
                'Lat: {:.6f}, Lng: {:.6f}<br><small>Updated: {}</small>',
                location.latitude, location.longitude,
                location.timestamp.strftime('%Y-%m-%d %H:%M:%S') if location.timestamp else 'Never'
            )
        return 'No GPS data'
    current_location_display.short_description = 'Current Location'


@admin.register(BusLocation)
class BusLocationAdmin(admin.ModelAdmin):
    list_display = (
        'bus', 'latitude', 'longitude', 'speed_display', 
        'is_moving', 'accuracy', 'timestamp'
    )
    list_filter = ('is_moving', 'is_at_terminal', 'timestamp')
    search_fields = ('bus__bus_number', 'terminal_name')
    readonly_fields = ('timestamp', 'map_link')
    date_hierarchy = 'timestamp'
    
    fieldsets = (
        ('Bus Information', {
            'fields': ('bus', 'timestamp')
        }),
        ('Location Data', {
            'fields': ('latitude', 'longitude', 'altitude', 'accuracy', 'map_link')
        }),
        ('Movement Data', {
            'fields': ('speed', 'heading', 'is_moving')
        }),
        ('Context', {
            'fields': ('is_at_terminal', 'terminal_name')
        }),
        ('Device Info', {
            'fields': ('device_id', 'battery_level'),
            'classes': ('collapse',)
        }),
    )
    
    def speed_display(self, obj):
        if obj.speed > 80:
            color = 'red'
        elif obj.speed > 60:
            color = 'orange'
        else:
            color = 'green'
        return format_html(
            '<span style="color: {};">{:.1f} km/h</span>',
            color, obj.speed
        )
    speed_display.short_description = 'Speed'
    
    def map_link(self, obj):
        if obj.latitude and obj.longitude:
            url = f"https://www.google.com/maps?q={obj.latitude},{obj.longitude}"
            return format_html(
                '<a href="{}" target="_blank">View on Google Maps</a>',
                url
            )
        return 'No coordinates'
    map_link.short_description = 'Map Link'


@admin.register(SpeedAlert)
class SpeedAlertAdmin(admin.ModelAdmin):
    list_display = (
        'bus', 'driver', 'alert_type', 'severity_display', 
        'recorded_speed', 'speed_limit', 'is_acknowledged', 'created_at'
    )
    list_filter = (
        'alert_type', 'severity', 'is_acknowledged', 
        'created_at'
    )
    search_fields = ('bus__bus_number', 'driver__user__username', 'message')
    readonly_fields = ('created_at', 'acknowledged_at', 'location_link')
    actions = ['mark_acknowledged']
    
    fieldsets = (
        ('Alert Information', {
            'fields': ('bus', 'driver', 'alert_type', 'severity', 'created_at')
        }),
        ('Speed Details', {
            'fields': ('recorded_speed', 'speed_limit', 'location', 'location_link')
        }),
        ('Alert Content', {
            'fields': ('message',)
        }),
        ('Acknowledgment', {
            'fields': ('is_acknowledged', 'acknowledged_by', 'acknowledged_at'),
            'classes': ('collapse',)
        }),
    )
    
    def severity_display(self, obj):
        colors = {
            'low': 'green',
            'medium': 'orange',
            'high': 'red',
            'critical': 'darkred'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.severity, 'black'), obj.get_severity_display()
        )
    severity_display.short_description = 'Severity'
    
    def location_link(self, obj):
        if obj.location:
            url = f"https://www.google.com/maps?q={obj.location.latitude},{obj.location.longitude}"
            return format_html(
                '<a href="{}" target="_blank">View Location</a>',
                url
            )
        return 'No location'
    location_link.short_description = 'Location'
    
    def mark_acknowledged(self, request, queryset):
        for alert in queryset:
            if not alert.is_acknowledged:
                alert.acknowledge(request.user)
        self.message_user(request, f'{queryset.count()} alerts marked as acknowledged.')
    mark_acknowledged.short_description = 'Mark selected alerts as acknowledged'


@admin.register(EmergencyAlert)
class EmergencyAlertAdmin(admin.ModelAdmin):
    list_display = (
        'bus', 'driver', 'alert_type', 'priority_display', 
        'is_resolved', 'authorities_contacted', 'created_at'
    )
    list_filter = (
        'alert_type', 'priority', 'is_resolved', 
        'authorities_contacted', 'created_at'
    )
    search_fields = ('bus__bus_number', 'driver__user__username', 'description')
    readonly_fields = ('created_at', 'resolved_at', 'response_time_minutes', 'location_link')
    actions = ['mark_resolved', 'contact_authorities']
    
    fieldsets = (
        ('Emergency Information', {
            'fields': ('bus', 'driver', 'alert_type', 'priority', 'created_at')
        }),
        ('Location', {
            'fields': ('location', 'location_link')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Response', {
            'fields': ('authorities_contacted', 'response_time_minutes')
        }),
        ('Resolution', {
            'fields': ('is_resolved', 'resolved_by', 'resolved_at', 'resolution_notes'),
            'classes': ('collapse',)
        }),
    )
    
    def priority_display(self, obj):
        colors = {
            'low': 'green',
            'medium': 'orange',
            'high': 'red',
            'critical': 'darkred'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.priority, 'black'), obj.get_priority_display()
        )
    priority_display.short_description = 'Priority'
    
    def location_link(self, obj):
        if obj.location:
            url = f"https://www.google.com/maps?q={obj.location.latitude},{obj.location.longitude}"
            return format_html(
                '<a href="{}" target="_blank">View Emergency Location</a>',
                url
            )
        return 'No location'
    location_link.short_description = 'Location'
    
    def mark_resolved(self, request, queryset):
        for alert in queryset:
            if not alert.is_resolved:
                alert.resolve(request.user, "Resolved via admin action")
        self.message_user(request, f'{queryset.count()} emergencies marked as resolved.')
    mark_resolved.short_description = 'Mark selected emergencies as resolved'
    
    def contact_authorities(self, request, queryset):
        queryset.update(authorities_contacted=True)
        self.message_user(request, f'Marked {queryset.count()} emergencies as having authorities contacted.')
    contact_authorities.short_description = 'Mark authorities as contacted'


@admin.register(RouteProgress)
class RouteProgressAdmin(admin.ModelAdmin):
    list_display = (
        'bus', 'route', 'status', 'progress_percentage', 
        'delay_minutes', 'journey_start_time'
    )
    list_filter = ('status', 'route', 'journey_start_time')
    search_fields = ('bus__bus_number', 'route__origin', 'route__destination')
    readonly_fields = ('created_at', 'updated_at', 'is_delayed')
    
    fieldsets = (
        ('Journey Information', {
            'fields': ('bus', 'route', 'status', 'journey_start_time')
        }),
        ('Timing', {
            'fields': ('estimated_arrival_time', 'actual_arrival_time', 'is_delayed')
        }),
        ('Progress', {
            'fields': ('distance_covered', 'total_distance', 'progress_percentage')
        }),
        ('Delays & Notes', {
            'fields': ('delay_minutes', 'delay_reason', 'driver_notes'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(GeofenceArea)
class GeofenceAreaAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'area_type', 'radius_meters', 'speed_limit',
        'alert_on_entry', 'alert_on_exit', 'is_active'
    )
    list_filter = ('area_type', 'is_active', 'alert_on_entry', 'alert_on_exit')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'map_link')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'area_type', 'is_active')
        }),
        ('Geographic Definition', {
            'fields': ('center_latitude', 'center_longitude', 'radius_meters', 'map_link')
        }),
        ('Monitoring Settings', {
            'fields': ('alert_on_entry', 'alert_on_exit', 'speed_limit')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def map_link(self, obj):
        if obj.center_latitude and obj.center_longitude:
            url = f"https://www.google.com/maps?q={obj.center_latitude},{obj.center_longitude}"
            return format_html(
                '<a href="{}" target="_blank">View Center on Google Maps</a>',
                url
            )
        return 'No coordinates'
    map_link.short_description = 'Map Link'
