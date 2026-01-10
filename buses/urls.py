from django.urls import path
from . import views

urlpatterns = [
    # --- Page Views ---
    path('search/', views.BusSearchView.as_view(), name='bus_search'),
    path('detail/<int:pk>/', views.BusDetailView.as_view(), name='bus_detail'),

    # --- Existing APIs ---
    path('api/routes/', views.get_routes_json, name='api_routes'),
    path('api/seats/<int:bus_id>/', views.get_available_seats, name='api_seats'),

    # --- ✅ NEW APIs (These connect to your new code) ---
    path('api/fare-preview/<int:bus_id>/', views.fare_preview_api, name='api_fare_preview'),
    path('api/live-location/<int:bus_id>/', views.live_location_api, name='api_live_location'),
]
