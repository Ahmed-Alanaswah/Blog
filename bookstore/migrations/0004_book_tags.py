# Generated by Django 4.0.1 on 2022-01-09 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0003_tag_order_book_order_customer_order_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='tags',
            field=models.ManyToManyField(to='bookstore.Tag'),
        ),
    ]
