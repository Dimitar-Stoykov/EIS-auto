from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eisauto', '0022_merge_0021s'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='galleryitem',
            name='title',
        ),
        migrations.RemoveField(
            model_name='galleryitem',
            name='description',
        ),
    ]
