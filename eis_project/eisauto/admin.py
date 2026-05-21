from django.contrib import admin
from .models import (
    SiteSettings,
    HomeHero,
    HomeBenefit,
    Service,
    HomePromo,
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
    list_display = ("title", "icon_image", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title",)
    fields = ("title", "description", "icon_image", "icon", "order", "is_active")


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


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "phone", "show_on_homepage", "order", "is_active")
    list_editable = ("show_on_homepage", "order", "is_active")
    list_filter = ("show_on_homepage", "is_active")
    search_fields = ("name", "address", "phone")
    fieldsets = (
        (None, {
            "fields": ("name", "address", "phone"),
        }),
        ("Работно време", {
            "fields": ("working_hours_text", "working_hours"),
        }),
        ("Google Maps", {
            "fields": ("google_maps_embed", "google_maps_url"),
            "description": (
                "Отвори Google Maps → намери мястото → бутон „Сподели" 
                "→ „Вграждане на карта" 
                "Готово — картата ще се покаже на сайта."
            ),
        }),
        ("Видимост", {
            "fields": ("show_on_homepage", "order", "is_active"),
        }),
    )