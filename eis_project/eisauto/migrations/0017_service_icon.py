from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eisauto', '0016_sitesettings_tiktok_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='icon',
            field=models.CharField(
                blank=True,
                default='bi-tools',
                help_text='Bootstrap Icons клас, напр. bi-tools, bi-speedometer2, bi-wrench, bi-droplet',
                max_length=60,
            ),
        ),
    ]
