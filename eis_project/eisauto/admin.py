from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from django.template.response import TemplateResponse
from django.utils.html import format_html
from .models import (
    AboutPage,
    ServicePage,
    SiteSettings,
    HomeHero,
    Service,
    HomePromo,
    Location,
    GalleryItem,
    GalleryPageSettings,
    PriceImage,
)


@admin.register(ServicePage)
class ServicePageAdmin(admin.ModelAdmin):
    list_display  = ('__str__', 'service_type', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    fieldsets = (
        ("Тип и видимост", {
            "fields": ("service_type", "is_active", "order"),
        }),
        ("Hero текст", {
            "fields": ("eyebrow", "hero_title", "hero_subtitle"),
        }),
        ("Съдържание", {
            "fields": ("section_title", "description", "address_detail"),
            "description": "Социалните мрежи се взимат от Настройки на сайта.",
        }),
    )


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Hero", {
            "fields": ("eyebrow", "hero_title", "hero_subtitle"),
        }),
        ("Съдържание", {
            "fields": ("section_title", "description", "founded_year", "address_detail"),
            "description": "Социалните мрежи се взимат автоматично от Настройки на сайта.",
        }),
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
    list_display = ("thumb", "__str__", "item_type", "duration", "order", "is_active")
    list_display_links = ("thumb", "__str__")
    list_editable = ("order", "is_active")
    list_filter = ("item_type", "is_active")
    fieldsets = (
        (None, {
            "fields": ("item_type", "order", "is_active"),
        }),
        ("Снимка", {
            "fields": ("image", "preview"),
            "description": "Попълнете само ако типът е 'Снимка'.",
        }),
        ("Видео", {
            "fields": ("video_file", "video_preview", "video_thumbnail", "duration"),
            "description": "Попълнете само ако типът е 'Видео'.",
        }),
    )
    readonly_fields = ("preview", "video_preview")

    @admin.display(description="Преглед на видеото")
    def video_preview(self, obj):
        if obj.video_file:
            return format_html(
                '<video src="{}" controls style="max-width:360px;max-height:280px;border-radius:8px;"></video>',
                obj.video_file.url,
            )
        return "—"

    @admin.display(description="Преглед")
    def thumb(self, obj):
        # Image items: show the image itself. Video items: show the
        # thumbnail if one was uploaded, otherwise a generic video icon
        # so the row is still visually distinguishable in the list.
        if obj.item_type == obj.TYPE_IMAGE and obj.image:
            return format_html(
                '<img src="{}" style="width:70px;height:52px;object-fit:cover;border-radius:6px;">',
                obj.image.url,
            )
        if obj.item_type == obj.TYPE_VIDEO and obj.video_thumbnail:
            return format_html(
                '<img src="{}" style="width:70px;height:52px;object-fit:cover;border-radius:6px;">',
                obj.video_thumbnail.url,
            )
        if obj.item_type == obj.TYPE_VIDEO and obj.video_file:
            return format_html(
                '<div style="width:70px;height:52px;display:flex;align-items:center;'
                'justify-content:center;background:#222;border-radius:6px;color:#fff;font-size:1.4rem;">'
                '<i class="bi bi-camera-reels"></i></div>'
            )
        return "—"

    @admin.display(description="Преглед на снимката")
    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:320px;max-height:320px;border-radius:8px;">', obj.image.url)
        return "—"

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


@admin.register(PriceImage)
class PriceImageAdmin(admin.ModelAdmin):
    list_display  = ('thumb', '__str__', 'order', 'is_active', 'created_at')
    list_display_links = ('thumb', '__str__')
    list_editable = ('order', 'is_active')
    list_filter   = ('is_active',)
    readonly_fields = ('preview',)
    fields = ('image', 'preview', 'caption', 'order', 'is_active')

    @admin.display(description="Преглед")
    def thumb(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:70px;height:52px;object-fit:cover;border-radius:6px;">',
                obj.image.url,
            )
        return "—"

    @admin.display(description="Преглед на снимката")
    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:320px;max-height:320px;border-radius:8px;">', obj.image.url)
        return "—"

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                "bulk-upload/",
                self.admin_site.admin_view(self.bulk_upload_view),
                name="eisauto_priceimage_bulk_upload",
            ),
        ]
        return custom + urls

    def bulk_upload_view(self, request):
        if request.method == "POST":
            files = request.FILES.getlist("images")
            if not files:
                messages.error(request, "Не са избрани снимки.")
            else:
                for f in files:
                    PriceImage.objects.create(image=f, is_active=True)
                messages.success(request, f"Качени {len(files)} ценови снимки.")
                return redirect("..")

        context = {
            **self.admin_site.each_context(request),
            "title": "Качи ценови снимки наведнъж",
            "opts": self.model._meta,
        }
        return TemplateResponse(
            request,
            "admin/eisauto/priceimage/bulk_upload.html",
            context,
        )

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['bulk_upload_url'] = 'admin:eisauto_priceimage_bulk_upload'
        return super().changelist_view(request, extra_context=extra_context)


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