from django.db import models

class Route(models.Model):
    name = models.CharField(max_length=150)

    source_name = models.CharField(max_length=100)
    source_lat = models.FloatField()
    source_lng = models.FloatField()

    destination_name = models.CharField(max_length=100)
    destination_lat = models.FloatField()
    destination_lng = models.FloatField()

    distance_km = models.FloatField(default=0)
    estimated_duration = models.IntegerField(help_text="Minutes")

    polyline = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class RouteStop(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="stops")
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.route.name} → {self.name}"
