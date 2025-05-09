import json
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Place


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
