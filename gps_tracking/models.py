from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from buses.models import Bus
from routes.models import Route

User = get_user_model()


class Driver(models.Model):
    """Driver profile with GPS tracking capabilities"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    license_number = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=20)
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Current assignment
    assigned_bus = models.OneToOneField(
        Bus, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='current_driver'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Driver: {self.user.get_full_name()} - {self.license_number}"
    
    @property
    def current_location(self):
        """Get the driver's current location"""
        if self.assigned_bus:
            return self.assigned_bus.current_location
        return None
    
    @property
    def current_speed(self):
        """Get the driver's current speed"""
        if self.assigned_bus:
            latest_location = self.assigned_bus.location_history.order_by('-timestamp').first()
            return latest_location.speed if latest_location else 0
        return 0


class BusLocation(models.Model):
    """Real-time GPS location tracking for buses"""
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='location_history')
    latitude = models.DecimalField(max_digits=12, decimal_places=8)
    longitude = models.DecimalField(max_digits=12, decimal_places=8)
    altitude = models.FloatField(null=True, blank=True, help_text="Altitude in meters")
    speed = models.FloatField(default=0.0, help_text="Speed in km/h")
    heading = models.FloatField(null=True, blank=True, help_text="Direction in degrees (0-360)")
    accuracy = models.FloatField(null=True, blank=True, help_text="GPS accuracy in meters")
    
    # Location context
    is_moving = models.BooleanField(default=False)
    is_at_terminal = models.BooleanField(default=False)
    terminal_name = models.CharField(max_length=100, blank=True)
    
    # Tracking metadata
    timestamp = models.DateTimeField(auto_now_add=True)
    device_id = models.CharField(max_length=100, blank=True, help_text="GPS device or phone ID")
    battery_level = models.IntegerField(null=True, blank=True, help_text="Device battery percentage")
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['bus', 'timestamp']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"{self.bus.bus_name} at {self.latitude}, {self.longitude} ({self.timestamp})"
    
    def save(self, *args, **kwargs):
        # Update bus current location when saving
        super().save(*args, **kwargs)
        self.bus.current_latitude = self.latitude
        self.bus.current_longitude = self.longitude
        self.bus.last_location_update = self.timestamp
        self.bus.save(update_fields=['current_latitude', 'current_longitude', 'last_location_update'])


class SpeedAlert(models.Model):
    """Speed monitoring and alerts for driver safety"""
    ALERT_TYPE_CHOICES = [
        ('overspeed', 'Over Speed Limit'),
        ('reckless', 'Reckless Driving'),
        ('sudden_brake', 'Sudden Braking'),
        ('rapid_acceleration', 'Rapid Acceleration'),
        ('idle_too_long', 'Idle Too Long'),
    ]
    
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='speed_alerts')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='speed_alerts')
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPE_CHOICES)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='medium')
    
    # Speed details
    recorded_speed = models.FloatField(help_text="Speed at time of alert (km/h)")
    speed_limit = models.FloatField(help_text="Speed limit for the area (km/h)")
    location = models.ForeignKey(BusLocation, on_delete=models.CASCADE)
    
    # Alert details
    message = models.TextField()
    is_acknowledged = models.BooleanField(default=False)
    acknowledged_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='acknowledged_alerts'
    )
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.alert_type.title()} Alert for {self.bus.bus_name} - {self.recorded_speed}km/h"
    
    def acknowledge(self, user):
        """Mark alert as acknowledged"""
        self.is_acknowledged = True
        self.acknowledged_by = user
        self.acknowledged_at = timezone.now()
        self.save()


class RouteProgress(models.Model):
    """Track bus progress along assigned routes"""
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='route_progress')
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    
    # Journey details
    journey_start_time = models.DateTimeField()
    estimated_arrival_time = models.DateTimeField(null=True, blank=True)
    actual_arrival_time = models.DateTimeField(null=True, blank=True)
    
    # Progress tracking
    distance_covered = models.FloatField(default=0.0, help_text="Distance covered in km")
    total_distance = models.FloatField(help_text="Total route distance in km")
    progress_percentage = models.FloatField(default=0.0)
    
    # Status
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_transit', 'In Transit'),
        ('delayed', 'Delayed'),
        ('arrived', 'Arrived'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    
    # Delays and notes
    delay_minutes = models.IntegerField(default=0)
    delay_reason = models.TextField(blank=True)
    driver_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-journey_start_time']
    
    def __str__(self):
        return f"{self.bus.bus_name} - {self.route} ({self.status})"
    
    def calculate_progress(self):
        """Calculate progress percentage based on distance"""
        if self.total_distance > 0:
            self.progress_percentage = min((self.distance_covered / self.total_distance) * 100, 100)
        else:
            self.progress_percentage = 0
        return self.progress_percentage
    
    @property
    def is_delayed(self):
        """Check if the journey is delayed"""
        if self.estimated_arrival_time and timezone.now() > self.estimated_arrival_time:
            return self.status != 'arrived'
        return False


class GeofenceArea(models.Model):
    """Define geographical boundaries for monitoring"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    # Area definition (simple circular geofence)
    center_latitude = models.DecimalField(max_digits=12, decimal_places=8)
    center_longitude = models.DecimalField(max_digits=12, decimal_places=8)
    radius_meters = models.IntegerField(help_text="Radius in meters")
    
    # Monitoring settings
    is_active = models.BooleanField(default=True)
    alert_on_entry = models.BooleanField(default=False)
    alert_on_exit = models.BooleanField(default=False)
    speed_limit = models.FloatField(null=True, blank=True, help_text="Speed limit in km/h")
    
    # Area type
    AREA_TYPE_CHOICES = [
        ('terminal', 'Bus Terminal'),
        ('school_zone', 'School Zone'),
        ('hospital_zone', 'Hospital Zone'),
        ('residential', 'Residential Area'),
        ('highway', 'Highway'),
        ('maintenance', 'Maintenance Zone'),
    ]
    area_type = models.CharField(max_length=20, choices=AREA_TYPE_CHOICES, default='terminal')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.area_type})"
    
    def is_inside(self, latitude, longitude):
        """Check if coordinates are inside this geofence"""
        from math import radians, cos, sin, asin, sqrt
        
        # Haversine formula to calculate distance
        lat1, lon1 = float(self.center_latitude), float(self.center_longitude)
        lat2, lon2 = float(latitude), float(longitude)
        
        # Convert to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        
        # Calculate distance
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        distance_km = 6371 * c  # Radius of earth in kilometers
        distance_m = distance_km * 1000  # Convert to meters
        
        return distance_m <= self.radius_meters


class EmergencyAlert(models.Model):
    """Emergency alerts from buses/drivers"""
    ALERT_TYPES = [
        ('panic', 'Panic Button'),
        ('breakdown', 'Vehicle Breakdown'),
        ('accident', 'Accident'),
        ('medical', 'Medical Emergency'),
        ('security', 'Security Threat'),
        ('fire', 'Fire Emergency'),
    ]
    
    PRIORITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='emergency_alerts')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='emergency_alerts')
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS, default='high')
    
    # Location when alert was triggered
    location = models.ForeignKey(BusLocation, on_delete=models.CASCADE)
    
    # Alert details
    description = models.TextField()
    is_resolved = models.BooleanField(default=False)
    resolved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resolved_emergencies'
    )
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(blank=True)
    
    # Response tracking
    response_time_minutes = models.IntegerField(null=True, blank=True)
    authorities_contacted = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.alert_type.title()} - {self.bus.bus_name} ({self.priority})"
    
    def resolve(self, user, notes=""):
        """Mark emergency as resolved"""
        self.is_resolved = True
        self.resolved_by = user
        self.resolved_at = timezone.now()
        self.resolution_notes = notes
        
        # Calculate response time
        time_diff = self.resolved_at - self.created_at
        self.response_time_minutes = int(time_diff.total_seconds() / 60)
        
        self.save()
