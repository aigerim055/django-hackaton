# Generated by Django 4.1.3 on 2022-11-21 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bio', '0009_userprofile_cachback'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='cachback',
            new_name='cashback',
        ),
    ]
