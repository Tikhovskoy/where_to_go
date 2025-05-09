from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django.utils.html import format_html
from .models import Place, PlaceImage


class PlaceImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = PlaceImage
    extra = 1
    sortable_field_name = 'order'
    fields = ('preview', 'image', 'order')
    readonly_fields = ('preview',)

    def preview(self, obj):
        """
        Превью загруженной картинки (max-height:200px).
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
class PlaceAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'latitude', 'longitude')
    search_fields = ('title',)
    inlines = [PlaceImageInline]


@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    list_display = ('place', 'order', 'preview')
    list_filter = ('place',)
    ordering = ('place', 'order')
    readonly_fields = ('preview',)

    def preview(self, obj):
        """
        Превью картинки в списке PlaceImageAdmin.
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
    preview.short_description = 'Превью'
