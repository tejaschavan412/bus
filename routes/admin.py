from django.contrib import admin
from .models import Route, RouteStop

class RouteStopInline(admin.TabularInline):
    model = RouteStop
    extra = 1

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    inlines = [RouteStopInline]
    list_display = ("name", "source_name", "destination_name", "active")
