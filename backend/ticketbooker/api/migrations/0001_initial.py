# Generated by Django 4.1.13 on 2024-06-21 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('released_date', models.CharField(max_length=100)),
                ('language', models.CharField(max_length=100)),
                ('rating', models.CharField(max_length=100)),
            ],
        ),
    ]
