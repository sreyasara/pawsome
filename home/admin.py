from django.contrib import admin
from django.core.validators import MinValueValidator
from .models import Category, Pet
from django.utils.html import format_html


class PetInline(admin.TabularInline):
    model = Pet


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [PetInline]


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'image_preview']
    list_filter = ['category']
    search_fields = ['name', 'description']
    list_per_page = 20
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" alt="{}" style="max-height: 100px; max-width: 100px;" />',
                               obj.image.url, obj.name)
        else:
            return '(No image)'
