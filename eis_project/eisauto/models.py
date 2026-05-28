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
    tiktok_url = models.URLField(blank=True)

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
    icon = models.CharField(
        max_length=60,
        blank=True,
        default="bi-tools",
        help_text="Bootstrap Icons клас, напр. bi-tools, bi-speedometer2, bi-wrench, bi-droplet"
    )
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
    google_maps_embed = models.TextField(
        blank=True,
        help_text=(
            "Embed код за картата (iframe HTML). "
            "Google Maps -> Share -> Embed a map -> Copy HTML -> постави тук."
        ),
    )
    google_maps_url = models.URLField(
        blank=True,
        max_length=1000,
        help_text=(
            "Линк за бутона под картата. "
            "Google Maps -> Share -> Send a link -> Copy -> постави тук."
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
        """Link for the button below the map.

        Priority:
          1) The explicit `google_maps_url` field (recommended).
          2) Coords parsed from the embed URL's `pb` parameter.
          3) The embed URL itself as a last resort.
        """
        import re

        if self.google_maps_url:
            return self.google_maps_url

        url = self.embed_url
        if not url:
            return ""

        m = re.search(r"!2d(-?\d+\.\d+)!3d(-?\d+\.\d+)", url)
        if m:
            lng, lat = m.group(1), m.group(2)
            return f"https://www.google.com/maps/search/?api=1&query={lat}%2C{lng}"
        return url
