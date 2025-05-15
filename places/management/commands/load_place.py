import os

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from places.models import Place, PlaceImage


class Command(BaseCommand):
    help = "Load a place from a JSON URL into the database"

    def add_arguments(self, parser):
        parser.add_argument("url", help="URL to the JSON file describing a place")

    def handle(self, *args, **options):
        url = options["url"]
        self.stdout.write(f'Fetching JSON from {url}…')
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            place_payload = resp.json()
        except Exception as e:
            raise CommandError(f"Error fetching or parsing JSON: {e}")

        title = place_payload.get("title") or place_payload.get("name")
        if not title:
            raise CommandError('JSON has no "title" field')

        coords = place_payload.get("coordinates", {})
        try:
            lng = float(coords["lng"])
            lat = float(coords["lat"])
        except Exception:
            raise CommandError("Invalid or missing coordinates in JSON")

        short_description = (
            place_payload.get("description_short")
            or place_payload.get("description")
            or ""
        )
        long_description = (
            place_payload.get("description_long")
            or place_payload.get("description_html")
            or ""
        )

        with transaction.atomic():
            place, created = Place.objects.update_or_create(
                title=title,
                defaults={
                    "short_description": short_description,
                    "long_description": long_description,
                    "longitude": lng,
                    "latitude": lat,
                },
            )
            operation_status = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f'{operation_status} place: {place.title}'))

            place.images.all().delete()
            imgs = place_payload.get("imgs", [])
            if not isinstance(imgs, list):
                raise CommandError('"imgs" must be a list')

            for idx, img_url in enumerate(imgs, start=1):
                self.stdout.write(f'  Downloading image {idx}/{len(imgs)}: {img_url}')
                try:
                    img_resp = requests.get(img_url)
                    img_resp.raise_for_status()
                except Exception as e:
                    raise CommandError(f"Error fetching image: {e}")

                img_name = os.path.basename(img_url.split("?")[0])
                django_file = ContentFile(img_resp.content, name=img_name)
                PlaceImage.objects.create(
                    place=place,
                    image=django_file,
                    order=idx,
                )

            self.stdout.write(self.style.SUCCESS(
                f'Loaded {len(imgs)} images for "{place.title}"'
            ))
