import json
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse  
from .models import Place

def start_page(request):
    """
    Собираем все места из БД в GeoJSON и рендерим стартовую страницу.
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

    return render(request, 'start.html', {
        'places_geojson': json.dumps(geojson, ensure_ascii=False),
        'show_debug_toggle': settings.DEBUG,
    })


def place_detail(request, pk):
    """
    API endpoint to return JSON details of a place.
    """
    place = get_object_or_404(Place, pk=pk)
    data = {
        'title': place.title,
        'imgs': [img.image.url for img in place.images.all()],
        'description_short': place.description_short,
        'description_long': place.description_long,
    }
    return JsonResponse(data, json_dumps_params={'ensure_ascii': False, 'indent': 2})
