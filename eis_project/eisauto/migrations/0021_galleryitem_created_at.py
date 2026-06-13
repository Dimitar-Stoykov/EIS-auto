from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('eisauto', '0020_gallerypagesettings_show_stats'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryitem',
            name='created_at',
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name='Качено на',
            ),
            preserve_default=False,
        ),
        migrations.AlterModelOptions(
            name='galleryitem',
            options={
                'ordering': ['-created_at'],
                'verbose_name': 'Gallery Item',
                'verbose_name_plural': 'Gallery Items',
            },
        ),
    ]
