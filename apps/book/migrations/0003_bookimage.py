# Generated by Django 4.1.3 on 2022-11-21 18:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_alter_author_options_alter_book_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='media')),
                ('avatar', models.ImageField(upload_to='media')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_images', to='book.book')),
            ],
        ),
    ]
