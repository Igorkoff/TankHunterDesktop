# Generated by Django 4.0 on 2022-12-11 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0005_convoy_alter_report_options_alter_report_civilians_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='convoy',
            options={'ordering': ['-tracking'], 'verbose_name': 'Convoy', 'verbose_name_plural': 'Convoys'},
        ),
        migrations.AlterModelOptions(
            name='report',
            options={'ordering': ['-verified'], 'verbose_name': 'Report', 'verbose_name_plural': 'Reports'},
        ),
    ]