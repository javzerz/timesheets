# Generated by Django 2.0.4 on 2018-07-29 03:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20180728_2313'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timecard',
            old_name='author',
            new_name='user',
        ),
    ]
