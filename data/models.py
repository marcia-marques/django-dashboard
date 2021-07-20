from django.db import models
import pandas as pd


class Campaign(models.Model):

    name = models.CharField(max_length=25)
    description = models.TextField(max_length=300)
    latitude = models.DecimalField(max_digits=13, decimal_places=9)
    longitude = models.DecimalField(max_digits=13, decimal_places=9)
    picture = models.ImageField(upload_to='pictures/')
    file = models.FileField(upload_to='files/')
    start_date = models.DateField(max_length=20, blank=True, null=True)
    end_date = models.DateField(max_length=20, blank=True, null=True)
    var1 = models.CharField(max_length=10, blank=True, null=True)
    var2 = models.CharField(max_length=10, blank=True, null=True)
    mylist = models.TextField(max_length=150, blank=True, null=True)

    def save(self, *args, **kwargs):
        df = pd.read_csv(self.file)
        df['DATE_TIME'] = pd.to_datetime(df.DATE_TIME)
        self.start_date = df.DATE_TIME.min().strftime('%Y-%m-%d')
        self.end_date = df.DATE_TIME.max().strftime('%Y-%m-%d')
        self.var1 = [x for x in df.columns if 'CO2_dry' in x][0]
        self.var2 = [x for x in df.columns if 'CH4_dry' in x][0]

        mylist = str(list(df.columns))
        mapping = [('[', ''), (']', ''), ("'", ''), (' ', '')]
        for k, v in mapping:
            mylist = mylist.replace(k, v)
        self.mylist = mylist

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
