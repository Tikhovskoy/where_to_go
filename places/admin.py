import traceback

from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django import forms
from django.contrib import admin
from django.utils.html import format_html
from tinymce.widgets import TinyMCE

from .models import Place, PlaceImage


class PlaceForm(forms.ModelForm):
    long_description = forms.CharField(
        label='Полное описание',
        widget=TinyMCE(attrs={'cols': 80, 'rows': 30})
    )

    class Meta:
        model = Place
        fields = '__all__'


class PlaceImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = PlaceImage
    extra = 1
    sortable_field_name = 'order'
    fields = ('preview', 'image', 'order')
    readonly_fields = ('preview',)

    def preview(self, obj):
        """
        Мини-превью картинки в inline.
        """
        try:
            if obj.image and hasattr(obj.image, 'url'):
                return format_html(
                    '<img src="{}" style="max-height:200px; max-width:100%; object-fit: contain;" />',
                    obj.image.url
                )
        except Exception:
            traceback.print_exc()
        return ""
    preview.short_description = 'Предпросмотр'


@admin.register(Place)
class PlaceAdmin(SortableAdminMixin, admin.ModelAdmin):
    form = PlaceForm
    list_display = ('title', 'latitude', 'longitude')
    search_fields = ('title',)
    inlines = [PlaceImageInline]


@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    list_display = ('place', 'order', 'preview')
    list_filter = ('place',)
    ordering = ('place', 'order')
    readonly_fields = ('preview',)
    autocomplete_fields = ['place']

    def preview(self, obj):
        """
        Превью для списка PlaceImageAdmin.
        """
        try:
            if obj.image and hasattr(obj.image, 'url'):
                return format_html(
                    '<img src="{}" style="max-height:200px; max-width:100%; object-fit: contain;" />',
                    obj.image.url
                )
        except Exception:
            traceback.print_exc()
        return ""
    preview.short_description = 'Предпросмотр'
