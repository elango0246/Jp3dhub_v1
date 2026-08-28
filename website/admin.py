from django.contrib import admin
from .models import ContactMessage, Gallery, Material, PricingPlan, Product, Service, Testimonial


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'material', 'price', 'available', 'featured', 'updated_at')
    list_filter = ('available', 'featured', 'category', 'material')
    search_fields = ('name', 'description', 'category', 'material')
    ordering = ('-featured', '-updated_at')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order', 'active')
    list_filter = ('active',)
    search_fields = ('name', 'description')
    ordering = ('display_order', 'name')


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'active')
    list_filter = ('active',)
    search_fields = ('name', 'description')


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'media_type', 'active', 'created_at')
    list_filter = ('media_type', 'active')
    search_fields = ('title',)
    ordering = ('-created_at',)


@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'featured', 'active')
    list_filter = ('featured', 'active')
    search_fields = ('name', 'features')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'role', 'rating', 'active', 'created_at')
    list_filter = ('active', 'rating')
    search_fields = ('customer_name', 'role', 'description')
    ordering = ('-created_at',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'service', 'created_at', 'is_read')
    list_filter = ('is_read', 'service', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
