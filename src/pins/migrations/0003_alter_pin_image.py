# Generated by Django 4.2.13 on 2024-05-21 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pins', '0002_pin_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pin',
            name='image',
            field=models.ImageField(max_length=255, upload_to='pins/'),
        ),
    ]