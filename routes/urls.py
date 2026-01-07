from django.urls import path
from . import views

app_name = "routes"

urlpatterns = [
    path("add/", views.add_route, name="add_route"),
    path("add-stop/", views.add_stop_to_route, name="add_stop"),
]
