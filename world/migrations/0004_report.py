# Generated by Django 4.0 on 2022-12-10 17:15

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0003_alter_user_last_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, editable=False, verbose_name='Comment')),
                ('image', models.ImageField(blank=True, editable=False, null=True, upload_to='photos/%Y/%m/%d/', verbose_name='Image')),
                ('civilians', models.CharField(choices=[('yes', 'Yes, there are some civilians.'), ('no', 'No, there are no civilians.'), ('unknown', "I don't know")], default='unknown', max_length=10, verbose_name='Civilians')),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326, verbose_name='Location')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='Time')),
                ('verified', models.BooleanField(default=False, verbose_name='Verified')),
                ('vehicles', models.CharField(blank=True, max_length=35, verbose_name='Vehicles')),
                ('user', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='world.user', verbose_name='User')),
            ],
            options={
                'verbose_name': 'Report',
                'verbose_name_plural': 'Reports',
                'ordering': ['-time', 'verified'],
            },
        ),
    ]
