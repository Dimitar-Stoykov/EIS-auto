
import os
import re
import mimetypes
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import StreamingHttpResponse, FileResponse, Http404, JsonResponse
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from .forms import ContactForm
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


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["site"] = SiteSettings.objects.first()

        context["hero"] = HomeHero.objects.filter(is_active=True).first()

        context["services"] = Service.objects.filter(
            is_active=True,
            show_on_homepage=True
        ).order_by("order")
        service_cards = [
            {
                "title": item.title,
                "description": item.short_description,
                "image_url": item.image.url if item.image else "",
                "icon": item.icon if item.icon else "bi-tools",
            }
            for item in context["services"]
        ]

        existing_titles = {item["title"] for item in service_cards}

        context["service_cards"] = service_cards[:6]

        context["promo"] = HomePromo.objects.filter(is_active=True)
        promo_cards = [
            {
                "title": item.title,
                "description": item.description,
                "image_url": item.image.url if item.image else "",
                "button_link": item.button_link,
                "badge": "Промоция",
            }
            for item in context["promo"]
        ]

        context["promo_cards"] = promo_cards

        context["locations"] = Location.objects.filter(
            is_active=True,
            show_on_homepage=True
        ).order_by("order")

        # Gallery preview on homepage (first 6 active images)
        context["gallery_preview"] = GalleryItem.objects.filter(
            is_active=True,
            item_type=GalleryItem.TYPE_IMAGE,
        ).order_by("-created_at")[:6]

        return context


GALLERY_INITIAL_IMAGES = 8
GALLERY_INITIAL_VIDEOS = 4
GALLERY_PAGE_SIZE = 20


class GalleryView(TemplateView):
    template_name = "gallery.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["site"] = SiteSettings.objects.first()
        context["locations"] = Location.objects.filter(is_active=True).order_by("order")

        images_qs = GalleryItem.objects.filter(is_active=True, item_type=GalleryItem.TYPE_IMAGE).order_by("-created_at")
        videos_qs = GalleryItem.objects.filter(is_active=True, item_type=GalleryItem.TYPE_VIDEO).order_by("-created_at")

        context["gallery_images"]       = list(images_qs[:GALLERY_INITIAL_IMAGES])
        context["gallery_images_total"] = images_qs.count()
        context["gallery_videos"]       = list(videos_qs[:GALLERY_INITIAL_VIDEOS])
        context["gallery_videos_total"] = videos_qs.count()
        context["gallery_settings"]     = GalleryPageSettings.objects.first()
        context["initial_images"]       = GALLERY_INITIAL_IMAGES
        context["initial_videos"]       = GALLERY_INITIAL_VIDEOS
        return context


def gallery_more(request):
    """AJAX endpoint — returns rendered HTML for the next batch of gallery items."""
    item_type  = request.GET.get("type", "images")
    offset     = max(int(request.GET.get("offset", 0)), 0)
    limit      = GALLERY_PAGE_SIZE

    if item_type == "images":
        qs = GalleryItem.objects.filter(is_active=True, item_type=GalleryItem.TYPE_IMAGE).order_by("-created_at")
        template = "partials/gallery_image_items.html"
    else:
        qs = GalleryItem.objects.filter(is_active=True, item_type=GalleryItem.TYPE_VIDEO).order_by("-created_at")
        template = "partials/gallery_video_items.html"

    total   = qs.count()
    items   = list(qs[offset: offset + limit])
    html    = render_to_string(template, {"items": items})
    new_offset = offset + limit

    return JsonResponse({"html": html, "has_more": new_offset < total})


class _BaseView(TemplateView):
    """Shared context for all simple pages."""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["site"] = SiteSettings.objects.first()
        context["locations"] = Location.objects.filter(is_active=True).order_by("order")
        return context


class ServicePageView(_BaseView):
    template_name = "service_page.html"

    def get(self, request, service_type, **kwargs):
        from django.http import Http404
        try:
            page = ServicePage.objects.get(service_type=service_type, is_active=True)
        except ServicePage.DoesNotExist:
            raise Http404
        return self.render_to_response(self.get_context_data(page=page))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service_page'] = kwargs.get('page')
        return context


class AboutView(_BaseView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["about"] = AboutPage.objects.first()
        return context


class ServicesView(_BaseView):
    template_name = "services.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["services"] = Service.objects.filter(is_active=True).order_by("order")
        return context


class PricesView(_BaseView):
    template_name = "prices.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["price_images"] = PriceImage.objects.filter(is_active=True).order_by("order", "-created_at")
        return context


class ContactsView(_BaseView):
    template_name = "contacts.html"

    def get_context_data(self, form=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["locations"] = Location.objects.filter(is_active=True).order_by("order")
        context["form"] = form or ContactForm()
        return context

    def get(self, request, **kwargs):
        return self.render_to_response(self.get_context_data())

    def post(self, request, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            site = SiteSettings.objects.first()
            # Recipient is always the email set in SiteSettings (admin).
            site_email = (getattr(site, "email", "") or "").strip()
            site_email = site_email or getattr(settings, "DEFAULT_CONTACT_EMAIL", "")

            visitor_name = f"{d['first_name']} {d['last_name']}"

            subject = f"Ново запитване от {visitor_name}"
            body = (
                f"Име: {visitor_name}\n"
                f"Е-майл: {d['email']}\n"
                f"Телефон: {d.get('phone') or '—'}\n\n"
                f"Съобщение:\n{d['message']}"
            )

            sent = False
            if site_email:
                try:
                    email = EmailMessage(
                        subject=subject,
                        body=body,
                        # The technical From address must stay the authenticated
                        # site mailbox (SMTP providers reject/override a spoofed
                        # From), but the display name shows who filled the form.
                        from_email=f"{visitor_name} <{site_email}>",
                        to=[site_email],
                        # Owner's mail client "Reply" button goes straight to
                        # the visitor's real address.
                        reply_to=[d["email"]],
                    )
                    email.send(fail_silently=False)
                    sent = True
                except Exception:
                    sent = False

            ctx = self.get_context_data(form=ContactForm())
            ctx["form_sent"] = sent
            ctx["form_error"] = not sent
            return self.render_to_response(ctx)

        ctx = self.get_context_data(form=form)
        ctx["form_error"] = True
        return self.render_to_response(ctx)


def stream_media(request, path):
    """Serve media files with HTTP Range request support so videos can be seeked."""
    file_path = os.path.join(settings.MEDIA_ROOT, path)

    if not os.path.exists(file_path):
        raise Http404

    content_type, _ = mimetypes.guess_type(file_path)
    content_type = content_type or "application/octet-stream"
    file_size = os.path.getsize(file_path)

    range_header = request.META.get("HTTP_RANGE", "").strip()
    range_match = re.match(r"bytes=(\d+)-(\d*)", range_header) if range_header else None

    if range_match:
        first_byte = int(range_match.group(1))
        last_byte = int(range_match.group(2)) if range_match.group(2) else file_size - 1
        last_byte = min(last_byte, file_size - 1)
        length = last_byte - first_byte + 1

        def _iter_file(path, offset, size, chunk=8192):
            with open(path, "rb") as f:
                f.seek(offset)
                remaining = size
                while remaining > 0:
                    data = f.read(min(chunk, remaining))
                    if not data:
                        break
                    remaining -= len(data)
                    yield data

        response = StreamingHttpResponse(
            _iter_file(file_path, first_byte, length),
            status=206,
            content_type=content_type,
        )
        response["Content-Range"] = f"bytes {first_byte}-{last_byte}/{file_size}"
        response["Content-Length"] = str(length)
    else:
        response = FileResponse(open(file_path, "rb"), content_type=content_type)
        response["Content-Length"] = str(file_size)

    response["Accept-Ranges"] = "bytes"
    return response
