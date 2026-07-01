from django.contrib import admin

from .models import (
    SiteSettings,
    Category,
    Product,
    ProductImage,
    Service,
    ServiceImage,
    GalleryImage,
    Testimonial,
)


# ==========================================================
# Site Settings
# ==========================================================

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = (
        "site_name",
        "whatsapp_number",
        "email",
    )

    def has_add_permission(self, request):
        # Allow only one SiteSettings object
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# ==========================================================
# Category
# ==========================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "order",
    )

    search_fields = ("name",)

    list_editable = ("order",)

    prepopulated_fields = {
        "slug": ("name",)
    }


# ==========================================================
# Product Images
# ==========================================================

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


# ==========================================================
# Products
# ==========================================================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "price",
        "discount_price",
        "stock",
        "is_active",
        "is_featured",
    )

    list_filter = (
        "category",
        "is_active",
        "is_featured",
    )

    search_fields = (
        "name",
        "short_description",
        "description",
    )

    list_editable = (
        "stock",
        "is_active",
        "is_featured",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    inlines = [ProductImageInline]


# ==========================================================
# Service Images
# ==========================================================

class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 1


# ==========================================================
# Services
# ==========================================================

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "starting_price",
        "is_active",
        "is_featured",
        "order",
    )

    list_filter = (
        "is_active",
        "is_featured",
    )

    search_fields = (
        "name",
        "short_description",
        "description",
    )

    list_editable = (
        "order",
        "is_active",
        "is_featured",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    inlines = [ServiceImageInline]


# ==========================================================
# Gallery
# ==========================================================

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "is_active",
        "order",
        "uploaded_at",
    )

    list_filter = ("is_active",)

    search_fields = ("title",)

    list_editable = (
        "is_active",
        "order",
    )


# ==========================================================
# Testimonials
# ==========================================================

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = (
        "client_name",
        "location",
        "rating",
        "is_active",
        "created_at",
    )

    list_filter = (
        "rating",
        "is_active",
    )

    search_fields = (
        "client_name",
        "location",
        "review",
    )

    list_editable = ("is_active",)


# ==========================================================
# Admin Site Branding
# ==========================================================

admin.site.site_header = "Pool Store Administration"
admin.site.site_title = "Pool Store Admin"
admin.site.index_title = "Pool Store Management Dashboard"