# Generated by Django 3.0.7 on 2020-06-25 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='author',
        ),
    ]
