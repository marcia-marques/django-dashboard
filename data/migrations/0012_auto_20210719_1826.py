# Generated by Django 3.2.5 on 2021-07-19 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0011_campaign_columns'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='columns',
        ),
        migrations.AddField(
            model_name='campaign',
            name='mylist',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='end_date',
            field=models.DateField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='start_date',
            field=models.DateField(blank=True, max_length=20, null=True),
        ),
    ]
