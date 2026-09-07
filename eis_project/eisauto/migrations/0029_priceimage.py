from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eisauto', '0028_servicepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='prices/', verbose_name='Снимка с цени')),
                ('caption', models.CharField(blank=True, max_length=120, verbose_name='Надпис (незадължително)')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Ред')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активна')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Ценова снимка',
                'verbose_name_plural': 'Ценови снимки',
                'ordering': ['order', '-created_at'],
            },
        ),
    ]
