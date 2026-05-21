
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

        context["promo"] = HomePromo.objects.filter(is_active=True)

        context["locations"] = Location.objects.filter(
            is_active=True,
            show_on_homepage=True
        ).order_by("order")

        return context