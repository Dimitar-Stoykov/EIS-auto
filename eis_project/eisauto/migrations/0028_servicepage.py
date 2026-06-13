from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eisauto', '0027_alter_aboutpage_eyebrow'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServicePage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_type', models.CharField(
                    choices=[
                        ('autoservice', 'Автосервиз'),
                        ('transport', 'Транспортни услуги'),
                        ('tires', 'Гумаджийница'),
                    ],
                    max_length=20,
                    unique=True,
                    verbose_name='Тип услуга',
                )),
                ('eyebrow', models.CharField(blank=True, max_length=80, verbose_name='Надпис над заглавието')),
                ('hero_title', models.CharField(max_length=160, verbose_name='Заглавие')),
                ('hero_subtitle', models.TextField(blank=True, verbose_name='Подзаглавие')),
                ('section_title', models.CharField(blank=True, max_length=160, verbose_name='Заглавие на секцията')),
                ('description', models.TextField(verbose_name='Описание')),
                ('address_detail', models.CharField(blank=True, max_length=255, verbose_name='Адрес')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активна')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Ред')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
