# Generated by Django 3.0.8 on 2020-07-28 04:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bitmex', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clientaccountcounter',
            old_name='subject',
            new_name='account',
        ),
    ]
