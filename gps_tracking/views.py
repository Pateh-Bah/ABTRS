from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, DetailView, View
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
import json

from buses.models import Bus
from .models import BusLocation, EmergencyAlert, SpeedAlert, RouteProgress


class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin to ensure only admin or staff users can access the view."""
    
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.is_admin or user.is_staff_member)


class BusTrackingMapView(TemplateView):
    """Public GPS tracking map showing all buses - accessible to all users."""
    template_name = 'gps_tracking/public_map.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY
        context['active_buses'] = Bus.objects.filter(is_active=True)
        return context


class BusDetailView(DetailView):
    """Detailed view of a specific bus with its GPS tracking info - accessible to all users."""
    model = Bus
    template_name = 'gps_tracking/bus_detail.html'
    context_object_name = 'bus'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bus = self.get_object()
        context['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY
        context['current_location'] = BusLocation.objects.filter(bus=bus).first()
        context['route_progress'] = RouteProgress.objects.filter(bus=bus).first()
        context['recent_alerts'] = SpeedAlert.objects.filter(
            bus=bus,
            created_at__gte=timezone.now() - timedelta(hours=24)
        ).order_by('-created_at')[:10]
        return context


class AdminGPSManagementView(AdminRequiredMixin, TemplateView):
    """Admin dashboard for GPS management."""
    template_name = 'gps_tracking/admin_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY
        context['total_buses'] = Bus.objects.filter(is_active=True).count()
        context['active_buses'] = Bus.objects.filter(
            is_active=True,
            location_history__timestamp__gte=timezone.now() - timedelta(minutes=30)
        ).count()
        context['recent_speed_alerts'] = SpeedAlert.objects.filter(
            is_acknowledged=False
        ).order_by('-created_at')[:5]
        context['recent_emergency_alerts'] = EmergencyAlert.objects.filter(
            is_resolved=False
        ).order_by('-created_at')[:5]
        return context


class AdminBusLocationListView(AdminRequiredMixin, ListView):
    """Admin view to list all bus locations."""
    model = BusLocation
    template_name = 'gps_tracking/admin_bus_list.html'
    context_object_name = 'bus_locations'
    paginate_by = 20
    
    def get_queryset(self):
        return BusLocation.objects.select_related('bus').order_by('-timestamp')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY
        return context


class SpeedAlertListView(AdminRequiredMixin, ListView):
    """Admin view to list speed alerts."""
    model = SpeedAlert
    template_name = 'gps_tracking/speed_alerts.html'
    context_object_name = 'speed_alerts'
    paginate_by = 20
    
    def get_queryset(self):
        return SpeedAlert.objects.select_related('bus').order_by('-created_at')


class EmergencyAlertListView(AdminRequiredMixin, ListView):
    """Admin view to list emergency alerts."""
    model = EmergencyAlert
    template_name = 'gps_tracking/emergency_alerts.html'
    context_object_name = 'emergency_alerts'
    paginate_by = 20
    
    def get_queryset(self):
        return EmergencyAlert.objects.select_related('bus').order_by('-created_at')


class DriverDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard for bus drivers."""
    template_name = 'gps_tracking/driver_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY
        # Assuming the driver is associated with a bus (you may need to adjust this logic)
        try:
            driver_bus = Bus.objects.filter(driver=self.request.user).first()
            if driver_bus:
                context['bus'] = driver_bus
                context['current_location'] = BusLocation.objects.filter(bus=driver_bus).first()
                context['route_progress'] = RouteProgress.objects.filter(bus=driver_bus).first()
        except:
            context['bus'] = None
        return context


# API Views
@method_decorator(csrf_exempt, name='dispatch')
class UpdateBusLocationAPIView(View):
    """API endpoint to update bus location - supports both bus ID and driver authentication."""
    
    def post(self, request, pk=None):
        try:
            # Support both direct bus ID and driver-based updates
            if pk:
                bus = get_object_or_404(Bus, pk=pk)
            else:
                # Try to find bus from authenticated driver
                if not request.user.is_authenticated:
                    return JsonResponse({'error': 'Authentication required'}, status=401)
                
                try:
                    from .models import Driver
                    driver = Driver.objects.get(user=request.user, is_active=True)
                    bus = driver.assigned_bus
                    if not bus:
                        return JsonResponse({'error': 'No bus assigned to driver'}, status=400)
                except Driver.DoesNotExist:
                    return JsonResponse({'error': 'Driver profile not found'}, status=404)
            
            data = json.loads(request.body)
            
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            speed = data.get('speed', 0)
            heading = data.get('heading', 0)
            accuracy = data.get('accuracy', None)
            
            if not latitude or not longitude:
                return JsonResponse({'error': 'Latitude and longitude are required'}, status=400)
            
            # Validate coordinates
            if not (-90 <= float(latitude) <= 90) or not (-180 <= float(longitude) <= 180):
                return JsonResponse({'error': 'Invalid coordinates'}, status=400)
            
            # Create new location entry (don't update, create history)
            bus_location = BusLocation.objects.create(
                bus=bus,
                latitude=latitude,
                longitude=longitude,
                speed=speed,
                heading=heading,
                accuracy=accuracy,
                is_moving=speed > 1  # Consider moving if speed > 1 km/h
            )
            
            # Update bus current location fields
            bus.current_latitude = latitude
            bus.current_longitude = longitude
            bus.last_location_update = timezone.now()
            bus.save(update_fields=['current_latitude', 'current_longitude', 'last_location_update'])
            
            # Check for speed violations (example: 80 km/h limit)
            if speed > 80:
                # Try to get or create driver for this bus
                try:
                    from .models import Driver
                    driver = Driver.objects.filter(assigned_bus=bus).first()
                    if driver:
                        SpeedAlert.objects.create(
                            bus=bus,
                            driver=driver,
                            alert_type='overspeed',
                            severity='high',
                            recorded_speed=speed,
                            speed_limit=80,
                            location=bus_location,
                            message=f"Speed limit exceeded: {speed} km/h (limit: 80 km/h)"
                        )
                except Exception as e:
                    print(f"Could not create speed alert: {e}")
            
            return JsonResponse({
                'success': True,
                'message': 'Location updated successfully',
                'location_id': bus_location.id,
                'timestamp': bus_location.timestamp.isoformat(),
                'bus_number': bus.bus_number
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except ValueError as e:
            return JsonResponse({'error': f'Invalid data: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class GetBusLocationsAPIView(View):
    """API endpoint to get all bus locations."""
    
    def get(self, request):
        try:
            # Get the most recent location for each active bus
            from django.db.models import Q
            
            # Get latest location for each bus
            latest_locations = []
            active_buses = Bus.objects.filter(is_active=True)
            
            for bus in active_buses:
                latest_location = BusLocation.objects.filter(bus=bus).order_by('-timestamp').first()
                if latest_location:
                    latest_locations.append(latest_location)
            
            data = []
            for location in latest_locations:
                # Check if location is recent (within last 10 minutes)
                time_diff = timezone.now() - location.timestamp
                is_online = time_diff.total_seconds() < 600  # 10 minutes
                
                data.append({
                    'bus_id': location.bus.id,
                    'bus_number': location.bus.bus_number,
                    'bus_name': location.bus.bus_name,
                    'latitude': float(location.latitude),
                    'longitude': float(location.longitude),
                    'speed': float(location.speed),
                    'heading': float(location.heading) if location.heading else 0,
                    'timestamp': location.timestamp.isoformat(),
                    'is_moving': location.is_moving,
                    'is_online': is_online,
                    'accuracy': float(location.accuracy) if location.accuracy else None,
                    'route_name': location.bus.assigned_route.name if location.bus.assigned_route else None,
                    'minutes_ago': int(time_diff.total_seconds() / 60)
                })
            
            return JsonResponse({
                'success': True,
                'buses': data,
                'total_buses': len(data),
                'online_buses': sum(1 for bus in data if bus['is_online']),
                'timestamp': timezone.now().isoformat()
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class RouteProgressAPIView(View):
    """API endpoint to get route progress for a specific bus."""
    
    def get(self, request, pk):
        try:
            bus = get_object_or_404(Bus, pk=pk)
            progress = RouteProgress.objects.filter(bus=bus).first()
            
            if not progress:
                return JsonResponse({'error': 'No route progress found'}, status=404)
            
            data = {
                'bus_id': bus.id,
                'route_name': bus.route.name if bus.route else None,
                'current_stop': progress.current_stop,
                'progress_percentage': float(progress.progress_percentage),
                'estimated_arrival': progress.estimated_arrival.isoformat() if progress.estimated_arrival else None,
                'updated_at': progress.updated_at.isoformat()
            }
            
            return JsonResponse(data)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class TriggerEmergencyAlertAPIView(View):
    """API endpoint to trigger emergency alert."""
    
    def post(self, request, pk):
        try:
            bus = get_object_or_404(Bus, pk=pk)
            data = json.loads(request.body)
            
            alert_type = data.get('alert_type', 'general')
            message = data.get('message', 'Emergency alert triggered')
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            
            emergency_alert = EmergencyAlert.objects.create(
                bus=bus,
                alert_type=alert_type,
                message=message,
                latitude=latitude,
                longitude=longitude
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Emergency alert triggered successfully',
                'alert_id': emergency_alert.id
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


# Action Views
class AcknowledgeSpeedAlertView(AdminRequiredMixin, View):
    """Acknowledge a speed alert."""
    
    def post(self, request, pk):
        alert = get_object_or_404(SpeedAlert, pk=pk)
        alert.is_acknowledged = True
        alert.acknowledged_by = request.user
        alert.acknowledged_at = timezone.now()
        alert.save()
        
        messages.success(request, f'Speed alert for {alert.bus.bus_number} acknowledged.')
        return redirect('gps_tracking:admin_speed_alerts')


class ResolveEmergencyAlertView(AdminRequiredMixin, View):
    """Resolve an emergency alert."""
    
    def post(self, request, pk):
        alert = get_object_or_404(EmergencyAlert, pk=pk)
        alert.is_resolved = True
        alert.resolved_by = request.user
        alert.resolved_at = timezone.now()
        alert.save()
        
        messages.success(request, f'Emergency alert for {alert.bus.bus_number} resolved.')
        return redirect('gps_tracking:admin_emergency_alerts')


@method_decorator(csrf_exempt, name='dispatch')
class DriverLocationUpdateAPIView(View):
    """API endpoint for drivers to update their location."""
    
    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        try:
            from .models import Driver
            driver = Driver.objects.get(user=request.user, is_active=True)
            if not driver.assigned_bus:
                return JsonResponse({'error': 'No bus assigned'}, status=400)
            
            data = json.loads(request.body)
            
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            speed = data.get('speed', 0)
            heading = data.get('heading', 0)
            accuracy = data.get('accuracy', None)
            altitude = data.get('altitude', None)
            
            if not latitude or not longitude:
                return JsonResponse({'error': 'Latitude and longitude are required'}, status=400)
            
            # Validate coordinates
            if not (-90 <= float(latitude) <= 90) or not (-180 <= float(longitude) <= 180):
                return JsonResponse({'error': 'Invalid coordinates'}, status=400)
            
            # Create new location entry
            bus_location = BusLocation.objects.create(
                bus=driver.assigned_bus,
                latitude=latitude,
                longitude=longitude,
                speed=speed,
                heading=heading,
                accuracy=accuracy,
                altitude=altitude,
                is_moving=speed > 1
            )
            
            # Update bus current location
            driver.assigned_bus.current_latitude = latitude
            driver.assigned_bus.current_longitude = longitude  
            driver.assigned_bus.last_location_update = timezone.now()
            driver.assigned_bus.save(update_fields=['current_latitude', 'current_longitude', 'last_location_update'])
            
            return JsonResponse({
                'success': True,
                'message': 'Location updated successfully',
                'bus_number': driver.assigned_bus.bus_number,
                'timestamp': bus_location.timestamp.isoformat()
            })
            
        except Driver.DoesNotExist:
            return JsonResponse({'error': 'Driver profile not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class PassengerBusTrackingAPIView(View):
    """API endpoint for passengers to get bus locations for specific routes."""
    
    def get(self, request):
        try:
            route_id = request.GET.get('route_id')
            bus_number = request.GET.get('bus_number')
            
            # Base queryset for active buses
            buses_query = Bus.objects.filter(is_active=True)
            
            # Filter by route if specified
            if route_id:
                buses_query = buses_query.filter(assigned_route_id=route_id)
            
            # Filter by bus number if specified
            if bus_number:
                buses_query = buses_query.filter(bus_number__icontains=bus_number)
            
            data = []
            for bus in buses_query:
                latest_location = BusLocation.objects.filter(bus=bus).order_by('-timestamp').first()
                if latest_location:
                    time_diff = timezone.now() - latest_location.timestamp
                    is_online = time_diff.total_seconds() < 600  # 10 minutes
                    
                    data.append({
                        'bus_id': bus.id,
                        'bus_number': bus.bus_number,
                        'bus_name': bus.bus_name,
                        'route_name': bus.assigned_route.name if bus.assigned_route else None,
                        'route_id': bus.assigned_route.id if bus.assigned_route else None,
                        'latitude': float(latest_location.latitude),
                        'longitude': float(latest_location.longitude),
                        'speed': float(latest_location.speed),
                        'heading': float(latest_location.heading) if latest_location.heading else 0,
                        'is_moving': latest_location.is_moving,
                        'is_online': is_online,
                        'last_update': latest_location.timestamp.isoformat(),
                        'minutes_ago': int(time_diff.total_seconds() / 60),
                        'driver_name': bus.driver.get_full_name() if hasattr(bus, 'driver') and bus.driver else 'No Driver Assigned'
                    })
            
            return JsonResponse({
                'success': True,
                'buses': data,
                'count': len(data),
                'filters': {
                    'route_id': route_id,
                    'bus_number': bus_number
                }
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@login_required
def driver_tracking(request):
    """Mobile-optimized driver tracking page for real-time location sharing"""
    try:
        # Get the driver's assigned bus
        driver = request.user
        bus = Bus.objects.filter(driver=driver).first()
        
        context = {
            'bus': bus,
            'driver': driver,
            'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        }
        
        return render(request, 'gps_tracking/driver_tracking.html', context)
    
    except Exception as e:
        messages.error(request, f"Error loading driver tracking: {str(e)}")
        return redirect('gps_tracking:driver_dashboard')