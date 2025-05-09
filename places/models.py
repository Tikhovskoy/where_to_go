from django.db import models

class Place(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    description_short = models.TextField(
        verbose_name='Краткое описание'
    )
    description_long = models.TextField(
        verbose_name='Полное описание'
    )
    latitude = models.FloatField(
        verbose_name='Широта'
    )
    longitude = models.FloatField(
        verbose_name='Долгота'
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.title


class PlaceImage(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Локация'
    )
    image = models.ImageField(
        upload_to='place_images/',
        verbose_name='Изображение'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок'
    )

    class Meta:
        ordering = ['order']
        verbose_name = 'Изображение места'
        verbose_name_plural = 'Изображения мест'

    def __str__(self):
        return f'{self.place.title} — фото #{self.order}'
