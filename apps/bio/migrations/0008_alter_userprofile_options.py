# Generated by Django 4.1.3 on 2022-11-17 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bio', '0007_rename_carousel_img_profileimage_avatar'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'User profile', 'verbose_name_plural': 'Users profiles'},
        ),
    ]
