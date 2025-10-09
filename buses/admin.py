from django.contrib import admin
from .models import Bus, Seat


class SeatInline(admin.TabularInline):
    model = Seat
    extra = 0


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = (
        "bus_name",
        "bus_number",
        "bus_type",
        "seat_capacity",
        "assigned_route",
        "assigned_driver_display",
        "available_seats",
        "is_active",
    )
    list_filter = ("bus_type", "is_active", "assigned_driver")
    search_fields = ("bus_name", "bus_number", "assigned_driver__user__first_name", "assigned_driver__user__last_name")
    list_editable = ("is_active",)
    inlines = [SeatInline]
    
    readonly_fields = ("current_latitude", "current_longitude", "last_location_update", "gps_device_id", "driver_info_display")
    
    fieldsets = (
        ("Basic Information", {
            "fields": ("bus_name", "bus_number", "bus_type", "seat_capacity", "is_active")
        }),
        ("Route & Driver Assignment", {
            "fields": ("assigned_route", "assigned_driver", "driver_info_display")
        }),
        ("GPS Tracking", {
            "fields": ("current_latitude", "current_longitude", "last_location_update", "gps_device_id"),
            "classes": ("collapse",)
        }),
        ("Legacy Driver Information", {
            "fields": ("current_driver_name", "current_driver_phone"),
            "classes": ("collapse",),
            "description": "These fields are deprecated. Use assigned_driver instead."
        }),
    )
    
    def assigned_driver_display(self, obj):
        if obj.assigned_driver:
            return f"{obj.assigned_driver.user.first_name} {obj.assigned_driver.user.last_name}"
        return "No driver assigned"
    assigned_driver_display.short_description = "Assigned Driver"
    
    def driver_info_display(self, obj):
        if obj.assigned_driver:
            driver = obj.assigned_driver
            return f"Driver: {driver.user.first_name} {driver.user.last_name}\nLicense: {driver.license_number}\nPhone: {driver.phone_number}"
        return "No driver assigned"
    driver_info_display.short_description = "Driver Information"


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ("bus", "seat_number", "is_window", "is_available")
    list_filter = ("bus", "is_window", "is_available")
    search_fields = ("bus__bus_name", "seat_number")
