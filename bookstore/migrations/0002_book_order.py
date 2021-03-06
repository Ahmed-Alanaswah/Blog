# Generated by Django 4.0.1 on 2022-01-09 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=190, null=True)),
                ('author', models.CharField(max_length=190, null=True)),
                ('price', models.FloatField(null=True)),
                ('categorey', models.CharField(choices=[('Classics.', 'Classics.'), ('Comic Book', 'Comic Book'), ('Fantasy', 'Fantasy'), ('Horror.', 'Horror.')], max_length=190, null=True)),
                ('description', models.CharField(max_length=200, null=True)),
                ('deate_created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deate_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Delivered', 'Delivered'), ('in Progress', 'in Progress'), ('Out of Oreder', 'Out of Order')], max_length=200, null=True)),
            ],
        ),
    ]
