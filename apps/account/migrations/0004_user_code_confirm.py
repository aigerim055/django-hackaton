# Generated by Django 4.1.3 on 2022-11-24 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='code_confirm',
            field=models.CharField(choices=[('email', 'email'), ('phone', 'phone')], default=1, max_length=6),
            preserve_default=False,
        ),
    ]
