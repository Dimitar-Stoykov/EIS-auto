
from django.views.generic import TemplateView
from .models import (
    SiteSettings,
    HomeHero,
    HomeBenefit,
    Service,
    HomePromo,
    Location,
)


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["site"] = SiteSettings.objects.first()

        context["hero"] = HomeHero.objects.filter(is_active=True).first()

        context["benefits"] = HomeBenefit.objects.filter(
            is_active=True
        ).order_by("order")

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


        return context
