# Generated by Django 3.0.7 on 2020-06-25 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20200625_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='detail',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.Detail'),
        ),
    ]