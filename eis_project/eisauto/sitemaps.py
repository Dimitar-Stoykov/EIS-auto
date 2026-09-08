from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import ServicePage


class StaticViewSitemap(Sitemap):
    """Pages with a fixed, parameter-free URL."""
    changefreq = 'weekly'

    def items(self):
        # Only URL names that actually resolve without extra arguments.
        return ['home_page', 'about', 'prices', 'gallery', 'contacts']

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        # Homepage gets the top priority, the rest share a slightly lower one.
        return 1.0 if item == 'home_page' else 0.7


class ServicePageSitemap(Sitemap):
    """One entry per active service page (autoservice / transport / tires)."""
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        return ServicePage.objects.filter(is_active=True)

    def location(self, obj):
        return obj.get_absolute_url()
