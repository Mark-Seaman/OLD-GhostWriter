# Generated by Django 4.0.5 on 2023-01-05 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publish', '0008_content_words'),
    ]

    operations = [
        migrations.AddField(
            model_name='pub',
            name='auto_contents',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pub',
            name='auto_index',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pub',
            name='auto_remove',
            field=models.BooleanField(default=False),
        ),
    ]
