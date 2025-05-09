from django.contrib import admin
from django.utils.html import format_html
from .models import Place, PlaceImage


class PlaceImageInline(admin.TabularInline):
    model = PlaceImage
    extra = 1
    fields = ('image', 'preview', 'order')
    readonly_fields = ('preview',)
    ordering = ('order',)

    def preview(self, obj):
        """
        Показывает превью загруженной картинки в админке.
        """
        try:
            if obj.image and hasattr(obj.image, 'url'):
                return format_html(
                    '<img src="{}" style="max-height:200px; width:auto;" />',
                    obj.image.url
                )
        except Exception:
            import traceback; print(traceback.format_exc())
        return ""
    preview.short_description = 'Предпросмотр'


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('title', 'latitude', 'longitude')
    search_fields = ('title',)
    inlines = [PlaceImageInline]


@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    list_display = ('place', 'order', 'image_tag')
    list_filter = ('place',)
    ordering = ('place', 'order')
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        """Показывает превью картинки в списке PlaceImageAdmin"""
        try:
            if obj.image and hasattr(obj.image, 'url'):
                return format_html(
                    '<img src="{}" style="max-height:200px; width:auto;" />',
                    obj.image.url
                )
        except Exception:
            import traceback; print(traceback.format_exc())
        return ""
    image_tag.short_description = 'Превью'
