from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eisauto', '0019_gallerypagesettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallerypagesettings',
            name='show_stats',
            field=models.BooleanField(
                default=True,
                verbose_name='Покажи статистики',
                help_text='Скрийте статистиките ако не искате да се показват в hero секцията.',
            ),
        ),
    ]
