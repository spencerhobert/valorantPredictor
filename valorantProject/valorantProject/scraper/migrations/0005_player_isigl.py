# Generated by Django 5.1 on 2024-08-24 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0004_remove_playermatchconnection_match_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='isIgl',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
