# Replace google_maps_url + google_maps_embed_url with lat/lng/zoom.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eisauto', '0010_delete_testimonial'),
    ]

    operations = [
        # Sofia city center as a safe default for any existing rows.
        migrations.AddField(
            model_name='location',
            name='latitude',
            field=models.DecimalField(
                max_digits=9,
                decimal_places=6,
                default=42.697708,
                help_text=(
                    'Географска ширина (latitude). Пример: 42.697708. '
                    'Намери я в Google Maps: десен клик върху точката → '
                    'първото число е latitude, второто longitude.'
                ),
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='location',
            name='longitude',
            field=models.DecimalField(
                max_digits=9,
                decimal_places=6,
                default=23.321868,
                help_text='Географска дължина (longitude). Пример: 23.321868.',
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='location',
            name='map_zoom',
            field=models.PositiveSmallIntegerField(
                default=15,
                help_text='Ниво на приближение (1–20). По-голямо число = по-близо.',
            ),
        ),
        migrations.RemoveField(
            model_name='location',
            name='google_maps_url',
        ),
        migrations.RemoveField(
            model_name='location',
            name='google_maps_embed_url',
        ),
    ]
