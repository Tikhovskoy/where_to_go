from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Place


def start_page(request):
    """
    Получает все локации из базы данных и формирует GeoJSON.
    Рендерит стартовую страницу со всеми локациями и их координатами.
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
                "detailsUrl": reverse("place-detail", args=[place.pk])
            }
        })

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    return render(request, "start.html", {
        "places_geojson": geojson,
        "show_debug_toggle": settings.DEBUG,
    })


def place_detail(request, pk):
    """
    Возвращает JSON с подробной информацией о месте.
    Оптимизировано с prefetch_related для загрузки изображений одним запросом.
    """
    place = get_object_or_404(
        Place.objects.prefetch_related("images"),
        pk=pk
    )
    place_serialized = {
        "title": place.title,
        "imgs": [img.image.url for img in place.images.all()],
        "description_short": place.short_description,
        "description_long": place.long_description,
    }
    return JsonResponse(place_serialized, json_dumps_params={"ensure_ascii": False, "indent": 2})
