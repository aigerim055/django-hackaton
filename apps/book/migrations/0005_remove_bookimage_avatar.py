# Generated by Django 4.1.3 on 2022-11-22 08:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_alter_book_description_alter_book_genre_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookimage',
            name='avatar',
        ),
    ]
