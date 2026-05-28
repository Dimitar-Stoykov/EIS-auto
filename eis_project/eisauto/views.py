
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
        # fallback_services = [
        #     ("Смяна на гуми", "Бърза и професионална смяна на летни и зимни гуми.", "bi-record-circle"),
        #     ("Спирачна система", "Диагностика и ремонт на спирачки за вашата безопасност.", "bi-disc"),
        #     ("Смяна на масла", "Масла и филтри от водещи производители.", "bi-droplet"),
        #     ("Диагностика", "Компютърна диагностика и откриване на неизправности.", "bi-speedometer2"),
        #     ("Ходова част", "Ремонт и поддръжка на ходова част и окачване.", "bi-sliders2"),
        #     ("Климатични системи", "Зареждане, проверка и ремонт на климатични системи.", "bi-snow"),
        # ]
        existing_titles = {item["title"] for item in service_cards}
        # for title, description, icon in fallback_services:
        #     if len(service_cards) >= 6:
        #         break
        #     if title not in existing_titles:
        #         service_cards.append({
        #             "title": title,
        #             "description": description,
        #             "image_url": "",
        #             "icon": icon,
        #         })
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
        # fallback_promos = [
        #     ("Смяна на гуми", "Професионална смяна на гуми с баланс и проверка на налягане.", "/media/home/promo/hero1.jpg", "-20%"),
        #     ("Спирачки комплект", "Спирачни дискове и накладки с монтаж.", "/media/home/promo/IMG_9070.jpg", "-15%"),
        #     ("Смяна на масло", "С включен маслен филтър и безплатна проверка.", "/media/home/promo/diagnostika.jfif", "-25%"),
        # ]
        promo_titles = {item["title"] for item in promo_cards}
        # for title, description, image_url, badge in fallback_promos:
        #     if len(promo_cards) >= 3:
        #         break
        #     if title not in promo_titles:
        #         promo_cards.append({
        #             "title": title,
        #             "description": description,
        #             "image_url": image_url,
        #             "button_link": f"tel:{context['site'].phone}",
        #             "badge": badge,
        #         })
        context["promo_cards"] = promo_cards

        context["locations"] = Location.objects.filter(
            is_active=True,
            show_on_homepage=True
        ).order_by("order")

        # gallery_preview = []
        # for item in context["promo"]:
        #     if item.image:
        #         gallery_preview.append({
        #             "image_url": item.image.url,
        #             "title": item.title,
        #         })
        #
        # for item in context["services"]:
        #     if item.image:
        #         gallery_preview.append({
        #             "image_url": item.image.url,
        #             "title": item.title,
        #         })

        # fallback_gallery = [
        #     ("/media/home/hero/hero1.jpg", "Автосервиз"),
        #     ("/media/home/promo/IMG_9070.jpg", "Работа в сервиза"),
        #     ("/media/home/promo/diagnostika.jfif", "Диагностика"),
        #     ("/media/home/promo/hero1.jfif", "Смяна на гуми"),
        # ]
        # existing_urls = {item["image_url"] for item in gallery_preview}
        # for image_url, title in fallback_gallery:
        #     if len(gallery_preview) >= 6:
        #         break
        #     if image_url not in existing_urls:
        #         gallery_preview.append({
        #             "image_url": image_url,
        #             "title": title,
        #         })

        # context["gallery_preview"] = gallery_preview[:6]

        return context
