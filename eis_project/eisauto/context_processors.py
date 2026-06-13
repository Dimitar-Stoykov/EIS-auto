from .models import ServicePage


def service_pages(request):
    return {
        'nav_service_pages': ServicePage.objects.filter(is_active=True).order_by('order'),
    }
