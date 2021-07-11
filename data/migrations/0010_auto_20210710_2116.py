# Generated by Django 3.2.5 on 2021-07-10 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0009_auto_20210710_2111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='columns',
        ),
        migrations.AlterField(
            model_name='campaign',
            name='end_date',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='start_date',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='var1',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='var2',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
