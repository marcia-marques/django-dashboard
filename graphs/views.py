from django.shortcuts import render
import pandas as pd

from data.models import Campaign
from .forms import DateRangeForm
from .mygraphs import time_series


def graphs_list(request):
    campaigns = Campaign.objects.all()
    context = {'campaigns': campaigns}
    return render(request, 'graphs/graphs_list.html', context)


def graphs_detail(request, id):
    campaign = Campaign.objects.get(id=id)

    # dataframe
    df = pd.read_csv(campaign.file)
    df['DATE_TIME'] = pd.to_datetime(df.DATE_TIME)

    # initial values
    start_date = df.DATE_TIME.min()
    end_date = df.DATE_TIME.max()

    initial_data = {'start_date': start_date,
                    'end_date': end_date}

    # form
    form = DateRangeForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

    # dataframe from range
    df = df.loc[(df.DATE_TIME >= start_date) & (df.DATE_TIME <= end_date)]

    script, div = time_series(df)
    context = {'campaign': campaign,
               'form': form,
               'script': script, 'div': div}
    return render(request, 'graphs/graphs_detail.html', context)
