from django.contrib import admin
from .models import Place, PlaceImage

class PlaceImageInline(admin.TabularInline):
    model = PlaceImage
    extra = 1
    fields = ('image', 'order')
    ordering = ('order',)

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('title', 'latitude', 'longitude')
    search_fields = ('title',)
    inlines = [PlaceImageInline]

@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    list_display = ('place', 'order', 'image')
    list_filter = ('place',)
    ordering = ('place', 'order')
