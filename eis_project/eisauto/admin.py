from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from django.template.response import TemplateResponse
from .models import (
    SiteSettings,
    HomeHero,
    Service,
    HomePromo,
    Location,
    GalleryItem,
    GalleryPageSettings,
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("company_name", "phone", "email")
    search_fields = ("company_name", "phone", "email")
    fieldsets = (
        (None, {
            "fields": ("company_name", "business_type"),
        }),
        ("Contacts", {
            "fields": ("phone", "email", "address"),
        }),
        ("Social media", {
            "fields": ("facebook_url", "instagram_url", "tiktok_url"),
            "description": (
                "Paste full profile URLs. Icons appear under the hero button. "
                "Empty field = icon hidden."
            ),
        }),
    )


@admin.register(HomeHero)
class HomeHeroAdmin(admin.ModelAdmin):
    list_display = ("title", "badge_text", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "subtitle")



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


@admin.register(GalleryPageSettings)
class GalleryPageSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Hero снимка", {
            "fields": ("hero_image",),
        }),
        ("Статистика", {
            "fields": (
                "show_stats",
                ("stat1_icon", "stat1_number", "stat1_label"),
                ("stat2_icon", "stat2_number", "stat2_label"),
                ("stat3_icon", "stat3_number", "stat3_label"),
            ),
        }),
    )


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ("__str__", "item_type", "duration", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("item_type", "is_active")
    fieldsets = (
        (None, {
            "fields": ("item_type", "order", "is_active"),
        }),
        ("Снимка", {
            "fields": ("image",),
            "description": "Попълнете само ако типът е 'Снимка'.",
        }),
        ("Видео", {
            "fields": ("video_file", "video_thumbnail", "duration"),
            "description": "Попълнете само ако типът е 'Видео'.",
        }),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                "bulk-upload/",
                self.admin_site.admin_view(self.bulk_upload_view),
                name="eisauto_galleryitem_bulk_upload",
            ),
            path(
                "bulk-upload-videos/",
                self.admin_site.admin_view(self.bulk_upload_videos_view),
                name="eisauto_galleryitem_bulk_upload_videos",
            ),
        ]
        return custom + urls

    def bulk_upload_view(self, request):
        if request.method == "POST":
            files = request.FILES.getlist("images")
            if not files:
                messages.error(request, "Не са избрани снимки.")
            else:
                created = 0
                for f in files:
                    GalleryItem.objects.create(
                        item_type=GalleryItem.TYPE_IMAGE,
                        image=f,
                        is_active=True,
                    )
                    created += 1
                messages.success(
                    request,
                    f"Успешно качени {created} снимки.",
                )
                return redirect("..")

        context = {
            **self.admin_site.each_context(request),
            "title": "Качи снимки наведнъж",
            "opts": self.model._meta,
        }
        return TemplateResponse(
            request,
            "admin/eisauto/galleryitem/bulk_upload.html",
            context,
        )

    def bulk_upload_videos_view(self, request):
        if request.method == "POST":
            files = request.FILES.getlist("videos")
            if not files:
                messages.error(request, "Не са избрани видео файлове.")
            else:
                created = 0
                for f in files:
                    GalleryItem.objects.create(
                        item_type=GalleryItem.TYPE_VIDEO,
                        video_file=f,
                        is_active=True,
                    )
                    created += 1
                messages.success(
                    request,
                    f"Успешно качени {created} видео файла.",
                )
                return redirect("..")

        context = {
            **self.admin_site.each_context(request),
            "title": "Качи видеа наведнъж",
            "opts": self.model._meta,
        }
        return TemplateResponse(
            request,
            "admin/eisauto/galleryitem/bulk_upload_videos.html",
            context,
        )


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
                "Embed: Share -> Embed a map -> Copy HTML. "
                "URL: Share -> Send a link -> Copy."
            ),
        }),
        ("Видимост", {
            "fields": ("show_on_homepage", "order", "is_active"),
        }),
    )