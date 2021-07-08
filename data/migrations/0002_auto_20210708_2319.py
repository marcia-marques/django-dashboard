# Generated by Django 3.2.5 on 2021-07-08 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('description', models.TextField(max_length=300)),
                ('latitude', models.DecimalField(decimal_places=9, max_digits=13)),
                ('longitude', models.DecimalField(decimal_places=9, max_digits=13)),
                ('picture', models.ImageField(upload_to='pictures/')),
                ('file', models.FileField(upload_to='files/')),
            ],
        ),
        migrations.DeleteModel(
            name='Data',
        ),
    ]
