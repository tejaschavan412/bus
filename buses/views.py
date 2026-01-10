from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.db import models
from datetime import datetime

# Import models - Assuming all are in the same folder
# If Booking is in a different app, we handle it below
from .models import Bus, Route, Stop, Trip

# ==========================
# 1. AUTHENTICATION (Register)
# ==========================

def register(request):
    """
    If your registration link points here, this function handles it.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now login.')
            return redirect('login') # Ensure you have a URL named 'login'
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


# ==========================
# 2. BUS PAGE VIEWS
# ==========================

class BusSearchView(ListView):
    model = Bus
    template_name = 'buses/search.html'
    context_object_name = 'buses'
    
    def get_queryset(self):
        # REMOVED 'driver' to prevent "Field does not exist" error
        queryset = Bus.objects.filter(is_active=True).select_related('route')
        
        source = self.request.GET.get('source', '')
        destination = self.request.GET.get('destination', '')
        bus_type = self.request.GET.get('bus_type', '')
        
        if source:
            queryset = queryset.filter(route__source__icontains=source)
        if destination:
            queryset = queryset.filter(route__destination__icontains=destination)
        if bus_type:
            queryset = queryset.filter(bus_type=bus_type)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['routes'] = Route.objects.filter(is_active=True)
        return context


class BusDetailView(DetailView):
    model = Bus
    template_name = 'buses/detail.html'
    context_object_name = 'bus'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bus = self.get_object()
        today = timezone.now().date()
        
        # Get current trip safely
        context['current_trip'] = Trip.objects.filter(bus=bus, date=today).first()
        
        if bus.route:
            context['stops'] = bus.route.stops.all()
        
        return context


# ==========================
# 3. API VIEWS (For Live Location & Fare)
# ==========================

def get_routes_json(request):
    routes = Route.objects.filter(is_active=True).values('id', 'source', 'destination', 'name')
    return JsonResponse(list(routes), safe=False)


def get_available_seats(request, bus_id):
    bus = get_object_or_404(Bus, pk=bus_id)
    date_str = request.GET.get('date', '')

    try:
        travel_date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else timezone.now().date()
    except ValueError:
        travel_date = timezone.now().date()

    # Try importing Booking from current models first
    try:
        from .models import Booking
    except ImportError:
        # If Booking is in a separate app named 'bookings'
        try:
            from bookings.models import Booking
        except ImportError:
            return JsonResponse({'error': 'Booking model not found'}, status=500)

    booked_seats = Booking.objects.filter(
        bus=bus,
        travel_date=travel_date,
        status__in=['confirmed', 'pending']
    ).aggregate(total=models.Sum('seats_booked'))['total'] or 0

    available = bus.total_seats - booked_seats

    return JsonResponse({
        'bus_id': bus_id,
        'total_seats': bus.total_seats,
        'booked_seats': booked_seats,
        'available_seats': available
    })


def fare_preview_api(request, bus_id):
    bus = get_object_or_404(Bus, pk=bus_id)
    source = request.GET.get('source')
    destination = request.GET.get('destination')

    # Safe access to base_fare (defaults to 0 if field missing)
    base_fare = getattr(bus, "base_fare", 0)

    estimated_fare = float(base_fare) * 1.0

    return JsonResponse({
        "bus_id": bus.id,
        "source": source,
        "destination": destination,
        "estimated_fare": estimated_fare
    })


def live_location_api(request, bus_id):
    bus = get_object_or_404(Bus, pk=bus_id)
    today = timezone.now().date()
    trip = Trip.objects.filter(bus=bus, date=today).first()

    # Safe attribute access using getattr
    latitude = getattr(trip, "current_latitude", None)
    longitude = getattr(trip, "current_longitude", None)
    status = getattr(trip, "status", None)

    return JsonResponse({
        "bus_id": bus.id,
        "latitude": latitude,
        "longitude": longitude,
        "status": status
    })
