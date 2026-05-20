from django.contrib import admin
from .models import (
    SiteSettings,
    HomeHero,
    HomeBenefit,
    Service,
    HomePromo,
    Testimonial,
    Location,
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("company_name", "phone", "email")
    search_fields = ("company_name", "phone", "email")


@admin.register(HomeHero)
class HomeHeroAdmin(admin.ModelAdmin):
    list_display = ("title", "badge_text", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "subtitle")


@admin.register(HomeBenefit)
class HomeBenefitAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "starting_price", "show_on_homepage", "order", "is_active")
    list_editable = ("starting_price", "show_on_homepage", "order", "is_active")
    list_filter = ("show_on_homepage", "is_active")
    search_fields = ("title", "short_description")
    ordering = ("order",)


@admin.register(HomePromo)
class HomePromoAdmin(admin.ModelAdmin):
    list_display = ("title", "button_text", "is_active")
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    search_fields = ("title", "description")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "rating", "source", "show_on_homepage", "order", "is_active")
    list_editable = ("rating", "show_on_homepage", "order", "is_active")
    list_filter = ("rating", "source", "show_on_homepage", "is_active")
    search_fields = ("customer_name", "text")


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "phone", "show_on_homepage", "order", "is_active")
    list_editable = ("show_on_homepage", "order", "is_active")
    list_filter = ("show_on_homepage", "is_active")
    search_fields = ("name", "address", "phone")