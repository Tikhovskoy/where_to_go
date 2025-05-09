import json
from django.shortcuts import render
from django.urls import reverse
from places.models import Place


def start_page(request):
    """
    Сбор локаций из базы данных и передача GeoJSON во фронтенд.
    """
    features = []
    for place in Place.objects.all():
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [place.longitude, place.latitude]
            },
            "properties": {
                "title": place.title,
                "placeId": place.pk,
                "detailsUrl": reverse('place-detail', args=[place.pk])
            }
        })
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    places_geojson = json.dumps(geojson, ensure_ascii=False)
    return render(request, 'start.html', {
        'places_geojson': places_geojson
    })
