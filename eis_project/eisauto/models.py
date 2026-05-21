from django.db import models

from django.db import models


class SiteSettings(models.Model):
    company_name = models.CharField(max_length=120)
    business_type = models.CharField(
        max_length=120,
        blank=True,
        null=True
    )



    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=255, blank=True)

    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return f"{self.company_name} {self.business_type}"


class HomeHero(models.Model):
    badge_text = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=160)
    title_second = models.CharField(max_length=160, blank=True)
    subtitle = models.TextField()
    hero_image = models.ImageField(upload_to="home/hero/")

    primary_button_text = models.CharField(max_length=50, default="Запази час")

    secondary_button_text = models.CharField(max_length=50, default="Виж услугите")
    secondary_button_link = models.CharField(max_length=255, default="#services")

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Home Hero"
        verbose_name_plural = "Home Hero"

    def __str__(self):
        return self.title


class HomeBenefit(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=180, blank=True)
    icon_image = models.ImageField(
        upload_to="home/benefits/",
        blank=True,
        null=True,
        help_text=(
            "Препоръчително: PNG или SVG, квадратно (1:1), "
            "прозрачен фон, около 80×80 px, златист/жълт цвят (#ffc107). "
            "Иконата се показва в кръгче 40×40 px."
        ),
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Резервен Bootstrap icon клас, напр.: bi-tools, bi-shield-check, bi-clock"
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Home Benefit"
        verbose_name_plural = "Home Benefits"

    def __str__(self):
        return self.title


class Service(models.Model):
    title = models.CharField(max_length=120)
    short_description = models.TextField()
    image = models.ImageField(upload_to="services/", blank=True, null=True)
    starting_price = models.CharField(max_length=50, blank=True)

    show_on_homepage = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.title


class HomePromo(models.Model):
    title = models.CharField(max_length=140)
    description = models.TextField()
    image = models.ImageField(upload_to="home/promo/", blank=True, null=True)

    button_text = models.CharField(max_length=50, default="Обади се")
    button_link = models.CharField(max_length=255, default="tel:+359")

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Home Promotion"
        verbose_name_plural = "Home Promotions"

    def __str__(self):
        return self.title



class Location(models.Model):
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=30, blank=True)
    working_hours_text = models.CharField(
        max_length=100,
        blank=True,
        default="ВСЕКИ ДЕН"
    )
    working_hours = models.TextField(blank=True)
    google_maps_url = models.URLField(
        help_text="Direct Google Maps link. Opens when user clicks button.",
        max_length=1000
    )
    google_maps_embed = models.TextField(
        blank=True,
        help_text=(
            "Постави Google Maps embed кода тук. "
            "Как: отвори Google Maps → намери мястото → бутон „Сподели"
            "(Share) → раздел „Вграждане на карта" 
            "копирай HTML и го постави цял тук. "
            "Може да поставиш и само линка от „Сподели → Копирай линк"
        ),
    )

    show_on_homepage = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def __str__(self):
        return self.name

    @property
    def embed_url(self):
        """Return the URL to use as the iframe `src`.

        Accepts either:
          - a full <iframe …src="…"…></iframe> snippet (we extract the src), or
          - a bare URL (we return it as-is).
        """
        import re

        value = (self.google_maps_embed or "").strip()
        if not value:
            return ""

        match = re.search(r'src=["\']([^"\']+)["\']', value)
        if match:
            return match.group(1)
        return value

    @property
    def maps_url(self):
        """Link for the „Виж в Google Maps" button.

        Extracts coordinates from the embed URL's `pb` parameter
        (format: …!2d{lng}!3d{lat}…) and builds a clean search URL
        that opens a normal Google Maps page with a pin at that point.

        Falls back to the embed URL itself if coords can't be parsed.
        """
        import re

        url = self.embed_url
        if not url:
            return ""

        # Embed pb format encodes longitude as !2d… and latitude as !3d…
        m = re.search(r"!2d(-?\d+\.\d+)!3d(-?\d+\.\d+)", url)
        if m:
            lng, lat = m.group(1), m.group(2)
            return f"https://www.google.com/maps/search/?api=1&query={lat}%2C{lng}"
        return url
