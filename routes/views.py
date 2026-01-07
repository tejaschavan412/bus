import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Route
from buses.models import Stop
from .forms import RouteForm


@csrf_exempt
def add_stop_to_route(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    data = json.loads(request.body)

    route_id = data.get("route_id")
    name = data.get("name")
    lat = data.get("latitude")
    lng = data.get("longitude")

    if not all([route_id, name, lat, lng]):
        return JsonResponse({"error": "Missing fields"}, status=400)

    route = get_object_or_404(Route, id=route_id)

    last_stop = route.stops.order_by("-sequence_number").first()
    next_seq = last_stop.sequence_number + 1 if last_stop else 1

    stop = Stop.objects.create(
        route=route,
        name=name,
        latitude=lat,
        longitude=lng,
        sequence_number=next_seq
    )

    return JsonResponse({
        "status": "success",
        "stop_id": stop.id,
        "sequence": stop.sequence_number
    })


def add_route(request):
    if request.method == "POST":
        form = RouteForm(request.POST)

        if form.is_valid():
            route = form.save()

            stops = json.loads(request.POST.get("stops_json", "[]"))

            for index, stop in enumerate(stops):
                Stop.objects.create(
                    route=route,
                    name=stop["name"],
                    latitude=stop["lat"],
                    longitude=stop["lng"],
                    sequence_number=index + 1
                )

            return redirect("routes:add_route")

    else:
        form = RouteForm()

    return render(request, "routes/add_route.html", {
        "form": form
    })
