# Generated by Django 5.1.6 on 2025-02-28 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_productspecification_key_features_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='specification',
            name='more_details',
            field=models.TextField(blank=True, null=True),
        ),
    ]
