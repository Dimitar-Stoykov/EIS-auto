# Make google_maps_url optional and clean up help_text on both maps fields.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eisauto', '0014_location_google_maps_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='google_maps_embed',
            field=models.TextField(
                blank=True,
                help_text=(
                    'Embed код за картата (iframe HTML). '
                    'Google Maps -> Share -> Embed a map -> Copy HTML -> постави тук.'
                ),
            ),
        ),
        migrations.AlterField(
            model_name='location',
            name='google_maps_url',
            field=models.URLField(
                blank=True,
                max_length=1000,
                help_text=(
                    'Линк за бутона под картата. '
                    'Google Maps -> Share -> Send a link -> Copy -> постави тук.'
                ),
            ),
        ),
    ]
