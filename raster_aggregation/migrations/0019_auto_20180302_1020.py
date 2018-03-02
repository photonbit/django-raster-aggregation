# Generated by Django 2.0.2 on 2018-03-02 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raster_aggregation', '0018_aggregationlayer_extent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aggregationlayer',
            name='name_column',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='aggregationlayer',
            name='shapefile',
            field=models.FileField(blank=True, null=True, upload_to='shapefiles/aggregationlayers'),
        ),
    ]
