# Generated by Django 4.1.3 on 2022-11-22 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_bookimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(related_name='books', to='book.genre'),
        ),
        migrations.AlterField(
            model_name='book',
            name='pages',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='book',
            name='year_published',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
