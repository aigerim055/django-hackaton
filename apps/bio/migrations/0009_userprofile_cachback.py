# Generated by Django 4.1.3 on 2022-11-21 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bio', '0008_alter_userprofile_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='cachback',
            field=models.PositiveIntegerField(default=0, verbose_name='cashback'),
        ),
    ]
