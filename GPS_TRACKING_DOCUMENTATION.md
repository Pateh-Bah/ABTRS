# GPS Tracking System - Waka-Fine Bus Booking

## Overview
The GPS Tracking System is a comprehensive real-time location monitoring solution for the Waka-Fine Bus Booking platform. It enables passengers to track bus locations, allows administrators to monitor fleet operations, and provides drivers with navigation and reporting tools.

## Features

### 🗺️ Public Bus Tracking
- **Real-time Map View**: Public interface for passengers to track bus locations
- **Bus Details**: Click on any bus to see detailed information including:
  - Current location and speed
  - Driver information
  - Route progress
  - Estimated arrival times
  - Recent location history

### 👨‍💼 Admin Management
- **GPS Dashboard**: Comprehensive overview of all bus locations and status
- **Bus Location Management**: Monitor all buses in real-time
- **Speed Alert Monitoring**: Track and acknowledge speed violations
- **Emergency Alert System**: Handle emergency situations and alerts
- **Geofence Management**: Define and monitor geographical boundaries

### 🚛 Driver Interface
- **Driver Dashboard**: Personalized interface for drivers
- **Location Reporting**: Automatic and manual location updates
- **Speed Monitoring**: Real-time speed tracking and alerts
- **Emergency Reporting**: Quick emergency alert system

## Technical Implementation

### Models
- **Driver**: Driver profiles with GPS tracking capabilities
- **BusLocation**: Real-time and historical location data
- **SpeedAlert**: Speed violation monitoring and alerts
- **RouteProgress**: Journey tracking and progress monitoring
- **GeofenceArea**: Geographical boundary definitions
- **EmergencyAlert**: Emergency situation management

### Extended Bus Model
The existing Bus model has been enhanced with GPS tracking fields:
- `current_latitude` / `current_longitude`: Current bus position
- `last_location_update`: Timestamp of last GPS update
- `gps_device_id`: Unique GPS device identifier
- `current_driver_name` / `current_driver_phone`: Active driver information

## Installation & Setup

### 1. Database Migration
```bash
python manage.py makemigrations gps_tracking
python manage.py migrate
```

### 2. Create Test Data
```bash
python manage.py create_gps_data
```

### 3. Configure Google Maps API (Optional)
Add your Google Maps API key to `settings.py`:
```python
GOOGLE_MAPS_API_KEY = 'your_api_key_here'
```

## URL Structure

### Public URLs
- `/gps/` - Public bus tracking map
- `/gps/bus/<id>/` - Detailed bus information

### Admin URLs
- `/gps/admin/` - GPS management dashboard
- `/gps/admin/buses/` - Bus location list
- `/gps/admin/speed-alerts/` - Speed alert management
- `/gps/admin/emergency-alerts/` - Emergency alert management

### Driver URLs
- `/gps/driver/` - Driver dashboard

### API Endpoints
- `/gps/api/bus/<id>/update-location/` - Update bus location
- `/gps/api/buses/locations/` - Get all bus locations
- `/gps/api/bus/<id>/progress/` - Route progress tracking
- `/gps/api/bus/<id>/emergency/` - Emergency alert trigger

## User Roles & Permissions

### 👥 Public Access
- View public bus tracking map
- See bus details and progress
- No registration required

### 👨‍💼 Admin Users (`role='admin'`)
- Full GPS management access
- Speed alert monitoring
- Emergency alert management
- Geofence configuration
- Driver management

### 🚛 Staff/Driver Users (`role='staff'` with Driver profile)
- Personal driver dashboard
- Location reporting capabilities
- Emergency alert system
- Speed monitoring

## Test Credentials

### Admin Access
- **Email**: admin@wakafine.com
- **Password**: admin123
- **Permissions**: Full GPS management

### Driver Access
- **Email**: driver1@wakafine.com / driver2@wakafine.com
- **Password**: driver123
- **Permissions**: Driver dashboard and reporting

## Features in Detail

### Real-Time Tracking
- GPS coordinates updated every 30 seconds (configurable)
- Historical location data stored for analysis
- Speed calculation and monitoring
- Movement status detection

### Speed Monitoring
- Configurable speed limits
- Automatic speed violation alerts
- Severity levels (low, medium, high)
- Admin acknowledgment system

### Emergency Alerts
- Driver-triggered emergency alerts
- Automatic alerts for unusual situations
- GPS coordinates included
- Admin resolution workflow

### Geofencing
- Circular geofence areas
- Entry/exit monitoring
- Speed limit enforcement within zones
- Multiple area types (terminal, school zone, etc.)

### Route Progress
- Real-time journey tracking
- Progress percentage calculation
- Distance covered monitoring
- Estimated arrival time calculation

## Security Features

- Role-based access control
- Authenticated API endpoints
- Driver profile verification
- Admin-only sensitive operations

## Browser Compatibility
- Modern browsers with JavaScript enabled
- Mobile-responsive design
- Google Maps integration
- Real-time updates via AJAX

## Development Notes

### Adding New Features
1. Extend models in `gps_tracking/models.py`
2. Create migrations: `python manage.py makemigrations gps_tracking`
3. Add views in `gps_tracking/views.py`
4. Update URL patterns in `gps_tracking/urls.py`
5. Create/update templates in `templates/gps_tracking/`

### GPS Data Integration
The system is designed to integrate with real GPS hardware devices. Location updates can be sent via:
- REST API endpoints
- Mobile app integration
- Hardware GPS device webhooks

### Customization
- Modify tracking intervals in view configurations
- Adjust speed limits in admin interface
- Customize map styling and markers
- Add new geofence area types

## Troubleshooting

### Common Issues
1. **Google Maps not loading**: Check API key configuration
2. **Location updates not working**: Verify API permissions
3. **Driver dashboard access denied**: Ensure driver profile exists
4. **Speed alerts not triggering**: Check speed limit configuration

### Database Issues
- Ensure all migrations are applied
- Check foreign key relationships
- Verify user roles and permissions

## Future Enhancements
- Real-time notifications via WebSocket
- Advanced analytics and reporting
- Integration with external GPS providers
- Mobile app development
- Predictive analytics for route optimization

---

## Support
For technical support or feature requests, contact the development team or refer to the main project documentation.