# Replace latitude/longitude/map_zoom with a single google_maps_embed text field.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eisauto', '0011_location_coordinates'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='google_maps_embed',
            field=models.TextField(
                blank=True,
                help_text=(
                    'Постави Google Maps embed кода тук. '
                    'Как: отвори Google Maps → намери мястото → бутон „Сподели" '
                    '(Share) → раздел „Вграждане на карта" (Embed a map) → '
                    'копирай HTML и го постави цял тук. '
                    'Може да поставиш и само линка от „Сподели → Копирай линк".'
                ),
            ),
        ),
        migrations.RemoveField(
            model_name='location',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='location',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='location',
            name='map_zoom',
        ),
    ]
