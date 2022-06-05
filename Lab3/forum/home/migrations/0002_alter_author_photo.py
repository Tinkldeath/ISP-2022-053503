# Generated by Django 4.0.5 on 2022-06-05 14:23

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='photo',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, default=None, force_format=None, keep_meta=True, null=True, quality=100, size=[50, 80], upload_to='authors'),
        ),
    ]
