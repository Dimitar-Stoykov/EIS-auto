from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eisauto', '0017_service_icon'),
    ]

    operations = [
        migrations.CreateModel(
            name='GalleryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_type', models.CharField(
                    choices=[('image', 'Снимка'), ('video', 'Видео')],
                    default='image',
                    max_length=10,
                    verbose_name='Тип',
                )),
                ('image', models.ImageField(
                    blank=True,
                    null=True,
                    upload_to='gallery/images/',
                    verbose_name='Снимка',
                    help_text='Качете снимка (JPG / PNG / WebP).',
                )),
                ('video_file', models.FileField(
                    blank=True,
                    null=True,
                    upload_to='gallery/videos/',
                    verbose_name='Видео файл',
                    help_text='MP4 файл.',
                )),
                ('video_thumbnail', models.ImageField(
                    blank=True,
                    null=True,
                    upload_to='gallery/thumbnails/',
                    verbose_name='Thumbnail за видеото',
                    help_text='Снимка, която се показва преди пускане на видеото.',
                )),
                ('title', models.CharField(
                    blank=True,
                    max_length=140,
                    verbose_name='Заглавие',
                    help_text='Показва се под видеото.',
                )),
                ('description', models.CharField(
                    blank=True,
                    max_length=220,
                    verbose_name='Описание',
                    help_text='Кратко описание под заглавието.',
                )),
                ('duration', models.CharField(
                    blank=True,
                    max_length=10,
                    verbose_name='Продължителност',
                    help_text='Напр.: 1:25',
                )),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Gallery Item',
                'verbose_name_plural': 'Gallery Items',
                'ordering': ['order', '-id'],
            },
        ),
    ]
