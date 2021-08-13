# Generated by Django 3.1 on 2021-08-13 10:14

import MainApp.formatChecker
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0005_auto_20210811_1839'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippet',
            name='public',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='image',
            field=MainApp.formatChecker.ContentTypeRestrictedFileField(blank=True, null=True, upload_to='images'),
        ),
    ]
