from django.contrib import admin
from django.core.validators import MinValueValidator

from auth_login.models import User
from .models import Category, Pet, Address, Review, Order, OrderItem
from django.utils.html import format_html

admin.site.register(User)


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
    readonly_fields = ['image_preview', 'seller']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" alt="{}" style="max-height: 100px; max-width: 100px;" />',
                               obj.image.url, obj.name)
        else:
            return '(No image)'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(seller=request.user)

    def save_model(self, request, obj, form, change):
        obj.seller = request.user
        obj.save()


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['item', 'order', ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(item__seller=request.user)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['pet', 'user', 'rating', ]
    list_filter = ['pet', 'user', 'rating', ]
    search_fields = ['pet', 'user', 'rating', ]
    list_per_page = 20

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(pet__seller=request.user)

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(Address)
admin.site.site_header = "Pet Shop Admin"
admin.site.site_title = "Pet Shop Admin Portal"
