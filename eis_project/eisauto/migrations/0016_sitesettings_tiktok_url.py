# Add tiktok_url URLField to SiteSettings.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eisauto', '0015_alter_location_google_maps_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='tiktok_url',
            field=models.URLField(blank=True),
        ),
    ]
