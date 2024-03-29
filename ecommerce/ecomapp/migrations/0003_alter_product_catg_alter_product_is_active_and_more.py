# Generated by Django 5.0.1 on 2024-02-08 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0002_rename_cat_product_catg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='catg',
            field=models.IntegerField(verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Available'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Product Name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_details',
            field=models.CharField(max_length=500, verbose_name='Product Details'),
        ),
    ]
