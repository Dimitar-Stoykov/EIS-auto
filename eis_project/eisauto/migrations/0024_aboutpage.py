from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eisauto', '0023_remove_galleryitem_title_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutPage',
            fields=[
                ('id',            models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hero_image',    models.ImageField(blank=True, null=True, upload_to='about/', verbose_name='Hero снимка')),
                ('eyebrow',       models.CharField(default='За нас', max_length=80, verbose_name='Надпис над заглавието')),
                ('hero_title',    models.CharField(default='Кои сме ние', max_length=160, verbose_name='Заглавие')),
                ('hero_subtitle', models.TextField(blank=True, verbose_name='Подзаглавие')),
                ('section_title', models.CharField(default='За компанията', max_length=160, verbose_name='Заглавие на секцията')),
                ('description',   models.TextField(verbose_name='Описание на компанията')),
                ('founded_year',  models.CharField(blank=True, max_length=10, verbose_name='Година на основаване')),
                ('address_detail',models.CharField(blank=True, max_length=255, verbose_name='Адрес (за страницата)')),
            ],
            options={
                'verbose_name': 'About Page',
                'verbose_name_plural': 'About Page',
            },
        ),
    ]
