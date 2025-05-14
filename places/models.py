from django.db import models
from django.urls import reverse


class Place(models.Model):
    title = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название"
    )
    short_description = models.TextField(
        verbose_name="Краткое описание",
        blank=True
    )
    long_description = models.TextField(
        verbose_name="Полное описание",
        blank=True
    )
    latitude = models.FloatField(
        verbose_name="Широта"
    )
    longitude = models.FloatField(
        verbose_name="Долгота"
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Место"
        verbose_name_plural = "Места"

    def __str__(self):
        return self.title

    def to_geojson_feature(self):
        return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [self.longitude, self.latitude],
            },
            "properties": {
                "id": self.pk,
                "title": self.title,
                "short_description": self.short_description,
                "long_description": self.long_description,
                "imgs": [img.image.url for img in self.images.order_by("order")],
                "detailsUrl": reverse("place-detail", args=[self.pk]),
            },
        }

    @classmethod
    def get_geojson(cls):
        return {
            "type": "FeatureCollection",
            "features": [place.to_geojson_feature() for place in cls.objects.all()],
        }


class PlaceImage(models.Model):
    place = models.ForeignKey(
        Place,
        related_name="images",
        on_delete=models.CASCADE,
        verbose_name="Место"
    )
    image = models.ImageField(
        upload_to="place_images/",
        verbose_name="Изображение"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок",
        db_index=True
    )

    class Meta:
        ordering = ["order"]
        verbose_name = "Изображение места"
        verbose_name_plural = "Изображения мест"

    def __str__(self):
        return f"{self.place.title} — фото #{self.order}"
