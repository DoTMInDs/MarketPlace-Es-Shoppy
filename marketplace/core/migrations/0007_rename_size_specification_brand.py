# Generated by Django 5.1.6 on 2025-02-28 21:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_specification_more_details'),
    ]

    operations = [
        migrations.RenameField(
            model_name='specification',
            old_name='size',
            new_name='brand',
        ),
    ]
