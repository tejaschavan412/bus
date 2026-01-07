from django import forms
from .models import Route

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = [
            "name",
            "source_name",
            "source_lat",
            "source_lng",
            "destination_name",
            "destination_lat",
            "destination_lng",
            "distance_km",
            "estimated_duration",
            "polyline",
            "active",
        ]

        widgets = {
            "source_lat": forms.HiddenInput(),
            "source_lng": forms.HiddenInput(),
            "destination_lat": forms.HiddenInput(),
            "destination_lng": forms.HiddenInput(),
            "polyline": forms.HiddenInput(),
        }
