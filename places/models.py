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

    def __str__(self):
        return self.title
