# Generated by Django 3.2.5 on 2021-07-10 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_campaign_min_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='min_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]