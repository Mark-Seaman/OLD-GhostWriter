# Generated by Django 4.0.5 on 2023-01-13 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publish', '0009_pub_auto_contents_pub_auto_index_pub_auto_remove'),
    ]

    operations = [
        migrations.AddField(
            model_name='pub',
            name='index_folders',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pub',
            name='index_months',
            field=models.BooleanField(default=False),
        ),
    ]
