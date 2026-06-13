from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eisauto', '0024_aboutpage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aboutpage',
            name='hero_image',
        ),
    ]
