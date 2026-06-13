from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eisauto', '0018_galleryitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='GalleryPageSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hero_image', models.ImageField(blank=True, null=True, upload_to='gallery/hero/', verbose_name='Hero снимка')),
                ('stat1_icon',   models.CharField(default='bi-tools',           max_length=60, verbose_name='Иконка 1')),
                ('stat1_number', models.CharField(default='1500+',              max_length=20, verbose_name='Число 1')),
                ('stat1_label',  models.CharField(default='ремонтирани автомобила', max_length=80, verbose_name='Надпис 1')),
                ('stat2_icon',   models.CharField(default='bi-hand-thumbs-up',  max_length=60, verbose_name='Иконка 2')),
                ('stat2_number', models.CharField(default='98%',                max_length=20, verbose_name='Число 2')),
                ('stat2_label',  models.CharField(default='доволни клиенти',    max_length=80, verbose_name='Надпис 2')),
                ('stat3_icon',   models.CharField(default='bi-award',           max_length=60, verbose_name='Иконка 3')),
                ('stat3_number', models.CharField(default='10+',                max_length=20, verbose_name='Число 3')),
                ('stat3_label',  models.CharField(default='години опит',        max_length=80, verbose_name='Надпис 3')),
            ],
            options={
                'verbose_name': 'Gallery Page Settings',
                'verbose_name_plural': 'Gallery Page Settings',
            },
        ),
    ]
