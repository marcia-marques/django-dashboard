# Generated by Django 3.2.5 on 2021-07-10 20:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0005_auto_20210710_2001'),
    ]

    operations = [
        migrations.RenameField(
            model_name='campaign',
            old_name='satart_date',
            new_name='start_date',
        ),
    ]
