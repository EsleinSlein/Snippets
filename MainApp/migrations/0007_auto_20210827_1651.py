# Generated by Django 3.1 on 2021-08-27 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0006_auto_20210813_1014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
    ]
