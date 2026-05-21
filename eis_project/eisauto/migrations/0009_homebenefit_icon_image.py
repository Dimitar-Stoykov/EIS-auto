# Generated for HomeBenefit.icon_image

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eisauto', '0008_location_working_hours_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='homebenefit',
            name='icon_image',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='home/benefits/',
                help_text=(
                    'Препоръчително: PNG или SVG, квадратно (1:1), '
                    'прозрачен фон, около 80×80 px, златист/жълт цвят (#ffc107). '
                    'Иконата се показва в кръгче 40×40 px.'
                ),
            ),
        ),
        migrations.AlterField(
            model_name='homebenefit',
            name='icon',
            field=models.CharField(
                blank=True,
                max_length=50,
                help_text='Резервен Bootstrap icon клас, напр.: bi-tools, bi-shield-check, bi-clock',
            ),
        ),
    ]
