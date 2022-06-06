# Generated by Django 4.0.5 on 2022-06-06 02:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_remove_tred_topics_tred_topic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='slug',
            field=models.SlugField(default=uuid.UUID('2d31d48f-8be1-46ce-938f-720da885a62e'), max_length=200),
        ),
        migrations.AlterField(
            model_name='topic',
            name='slug',
            field=models.SlugField(default=uuid.UUID('b83aeabd-66c8-45bf-959d-afb8f4e5da30'), max_length=200),
        ),
        migrations.AlterField(
            model_name='tred',
            name='slug',
            field=models.SlugField(default=uuid.UUID('99ebf2ca-2c5b-4d1e-87a7-fc00db3fc219'), max_length=200),
        ),
    ]