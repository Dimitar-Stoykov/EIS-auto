from django.db import models


class AboutPage(models.Model):
    """Content for the About page — edit once, reflected instantly."""

    # Hero
    eyebrow         = models.CharField(max_length=80,       verbose_name="Надпис над заглавието",blank=True)
    hero_title      = models.CharField(max_length=160, default="Кои сме ние",  verbose_name="Заглавие")
    hero_subtitle   = models.TextField(blank=True,                              verbose_name="Подзаглавие")

    # Main body — left column
    section_title   = models.CharField(max_length=160, default="За компанията", verbose_name="Заглавие на секцията")
    description     = models.TextField(verbose_name="Описание на компанията",
                                       help_text="Основният текст. Може да използвате празен ред за нов параграф.")
    founded_year    = models.CharField(max_length=10, blank=True, verbose_name="Година на основаване",
                                       help_text="Напр.: 2010")
    address_detail  = models.CharField(max_length=255, blank=True, verbose_name="Адрес (за страницата)")

    class Meta:
        verbose_name        = "About Page"
        verbose_name_plural = "About Page"

    def __str__(self):
        return "About Page"


class ServicePage(models.Model):
    TYPE_AUTOSERVICE = 'autoservice'
    TYPE_TRANSPORT   = 'transport'
    TYPE_TIRES       = 'tires'
    TYPE_CHOICES = [
        (TYPE_AUTOSERVICE, 'Автосервиз'),
        (TYPE_TRANSPORT,   'Транспортни услуги'),
        (TYPE_TIRES,       'Гумаджийница'),
    ]

    service_type   = models.CharField(max_length=20, choices=TYPE_CHOICES, unique=True, verbose_name="Тип услуга")
    eyebrow        = models.CharField(max_length=80,  blank=True, verbose_name="Надпис над заглавието")
    hero_title     = models.CharField(max_length=160,blank=True, verbose_name="Заглавие")
    hero_subtitle  = models.TextField(blank=True, verbose_name="Подзаглавие")
    section_title  = models.CharField(max_length=160, blank=True, verbose_name="Заглавие на секцията")
    description    = models.TextField(verbose_name="Описание")
    address_detail = models.CharField(max_length=255, blank=True, verbose_name="Адрес")
    is_active      = models.BooleanField(default=True, verbose_name="Активна")
    order          = models.PositiveIntegerField(default=0, verbose_name="Ред")

    class Meta:
        ordering = ['order']
        verbose_name = "Страница услуга"
        verbose_name_plural = "Страници услуги"

    def __str__(self):
        return self.get_service_type_display()

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('service_page', args=[self.service_type])


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



class GalleryPageSettings(models.Model):
    """Hero image and stats for the Gallery page."""
    hero_image = models.ImageField(
        upload_to="gallery/hero/",
        blank=True, null=True,
        verbose_name="Hero снимка",
        help_text="Снимката на колата вдясно в hero секцията.",
    )

    stat1_icon   = models.CharField(max_length=60, default="bi-tools",        verbose_name="Иконка 1", help_text="Bootstrap icon клас")
    stat1_number = models.CharField(max_length=20, default="1500+",            verbose_name="Число 1")
    stat1_label  = models.CharField(max_length=80, default="ремонтирани автомобила", verbose_name="Надпис 1")

    stat2_icon   = models.CharField(max_length=60, default="bi-hand-thumbs-up", verbose_name="Иконка 2")
    stat2_number = models.CharField(max_length=20, default="98%",               verbose_name="Число 2")
    stat2_label  = models.CharField(max_length=80, default="доволни клиенти",   verbose_name="Надпис 2")

    stat3_icon   = models.CharField(max_length=60, default="bi-award",          verbose_name="Иконка 3")
    stat3_number = models.CharField(max_length=20, default="10+",               verbose_name="Число 3")
    stat3_label  = models.CharField(max_length=80, default="години опит",       verbose_name="Надпис 3")

    show_stats = models.BooleanField(
        default=True,
        verbose_name="Покажи статистики",
        help_text="Скрийте статистиките ако не искате да се показват в hero секцията.",
    )

    class Meta:
        verbose_name = "Gallery Page Settings"
        verbose_name_plural = "Gallery Page Settings"

    def __str__(self):
        return "Gallery Page Settings"


class GalleryItem(models.Model):
    TYPE_IMAGE = "image"
    TYPE_VIDEO = "video"
    TYPE_CHOICES = [
        (TYPE_IMAGE, "Снимка"),
        (TYPE_VIDEO, "Видео"),
    ]

    item_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default=TYPE_IMAGE,
        verbose_name="Тип",
    )

    # ── Image ──────────────────────────────────────────────
    image = models.ImageField(
        upload_to="gallery/images/",
        blank=True,
        null=True,
        verbose_name="Снимка",
        help_text="Качете снимка (JPG / PNG / WebP).",
    )

    # ── Video ──────────────────────────────────────────────
    video_file = models.FileField(
        upload_to="gallery/videos/",
        blank=True,
        null=True,
        verbose_name="Видео файл",
        help_text="MP4 файл.",
    )
    video_thumbnail = models.ImageField(
        upload_to="gallery/thumbnails/",
        blank=True,
        null=True,
        verbose_name="Thumbnail за видеото",
        help_text="Снимка, която се показва преди пускане на видеото.",
    )
    duration = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="Продължителност",
        help_text="Напр.: 1:25",
    )

    # ── Meta ───────────────────────────────────────────────
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Качено на")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Gallery Item"
        verbose_name_plural = "Gallery Items"

    def __str__(self):
        return f"{self.get_item_type_display()} #{self.pk}"

    @property
    def image_url(self):
        if self.item_type == self.TYPE_IMAGE and self.image:
            return self.image.url
        if self.item_type == self.TYPE_VIDEO and self.video_thumbnail:
            return self.video_thumbnail.url
        return ""

    @property
    def video_url(self):
        if self.video_file:
            return self.video_file.url
        return ""


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
