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
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Example: bi-tools, bi-shield-check, bi-clock"
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


class Testimonial(models.Model):
    customer_name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(default=5)
    text = models.TextField()

    source = models.CharField(
        max_length=50,
        blank=True,
        help_text="Example: Google, Facebook, Website"
    )

    show_on_homepage = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"{self.customer_name} - {self.rating}/5"


class Location(models.Model):
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=30, blank=True)
    working_hours = models.TextField(blank=True)

    google_maps_url = models.URLField(
        help_text="Direct Google Maps link. Opens when user clicks button.",
        max_length=1000
    )
    google_maps_embed_url = models.URLField(
        help_text="Google Maps iframe embed URL."
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
