from django.db import models
from django.core.exceptions import ValidationError
from routes.models import Route


class Bus(models.Model):
    BUS_TYPE_CHOICES = [
        ("mini", "Mini Bus (14 seats)"),
        ("standard", "Standard Bus (25 seats)"),
        ("large", "Large Bus (35 seats)"),
    ]

    bus_number = models.CharField(max_length=20, unique=True)
    bus_name = models.CharField(max_length=100)
    bus_type = models.CharField(
        max_length=20, choices=BUS_TYPE_CHOICES, default="standard"
    )
    seat_capacity = models.PositiveIntegerField()
    assigned_route = models.ForeignKey(
        Route, on_delete=models.SET_NULL, null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    
    # GPS Tracking fields
    current_latitude = models.DecimalField(
        max_digits=12, 
        decimal_places=8, 
        null=True, 
        blank=True,
        help_text="Current GPS latitude"
    )
    current_longitude = models.DecimalField(
        max_digits=12, 
        decimal_places=8, 
        null=True, 
        blank=True,
        help_text="Current GPS longitude"
    )
    last_location_update = models.DateTimeField(
        null=True, 
        blank=True,
        help_text="Last time GPS location was updated"
    )
    gps_device_id = models.CharField(
        max_length=100, 
        blank=True,
        help_text="GPS device or tracking device ID"
    )
    
    # Driver assignment - ForeignKey to Driver model
    assigned_driver = models.ForeignKey(
        'gps_tracking.Driver',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_buses',
        help_text="Currently assigned driver for this bus"
    )
    
    # Legacy fields for backward compatibility (will be removed in future)
    current_driver_name = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Name of currently assigned driver (deprecated - use assigned_driver)"
    )
    current_driver_phone = models.CharField(
        max_length=20, 
        blank=True,
        help_text="Phone number of current driver (deprecated - use assigned_driver)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bus_name} ({self.bus_number})"

    @property
    def driver_name(self):
        """Get the name of the assigned driver"""
        if self.assigned_driver:
            return f"{self.assigned_driver.user.first_name} {self.assigned_driver.user.last_name}".strip()
        return self.current_driver_name or "No driver assigned"
    
    @property
    def driver_phone(self):
        """Get the phone number of the assigned driver"""
        if self.assigned_driver:
            return self.assigned_driver.phone_number
        return self.current_driver_phone or "N/A"
    
    @property
    def available_seats(self):
        from bookings.models import Booking
        from django.utils import timezone

        # Get today's bookings for this bus
        today_bookings = Booking.objects.filter(
            bus=self,
            travel_date__date=timezone.now().date(),
            status="confirmed",
        ).count()
        return self.seat_capacity - today_bookings
    
    @property
    def current_location(self):
        """Get current GPS coordinates as a dict"""
        if self.current_latitude and self.current_longitude:
            return {
                'latitude': float(self.current_latitude),
                'longitude': float(self.current_longitude),
                'last_update': self.last_location_update
            }
        return None
    
    @property
    def latest_speed(self):
        """Get the latest recorded speed from location history"""
        if hasattr(self, 'location_history'):
            latest = self.location_history.order_by('-timestamp').first()
            return latest.speed if latest else 0
        return 0
    
    @property
    def is_moving(self):
        """Check if bus is currently moving based on latest location data"""
        if hasattr(self, 'location_history'):
            latest = self.location_history.order_by('-timestamp').first()
            return latest.is_moving if latest else False
        return False
    
    def update_location(self, latitude, longitude, speed=0, **kwargs):
        """Update bus location and create location history record"""
        from django.utils import timezone
        
        self.current_latitude = latitude
        self.current_longitude = longitude
        self.last_location_update = timezone.now()
        self.save(update_fields=['current_latitude', 'current_longitude', 'last_location_update'])
        
        # Create location history record if gps_tracking app is available
        try:
            from gps_tracking.models import BusLocation
            BusLocation.objects.create(
                bus=self,
                latitude=latitude,
                longitude=longitude,
                speed=speed,
                **kwargs
            )
        except ImportError:
            # gps_tracking app not available
            pass


class Seat(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name="seats")
    seat_number = models.CharField(max_length=5)
    is_window = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ["bus", "seat_number"]

    def __str__(self):
        return f"{self.bus.bus_name} - Seat {self.seat_number}"
