from django.shortcuts import render
import pandas as pd
import numpy as np

from data.models import Campaign
from .forms import DateRangeModelForm
from .mygraphs import bokeh_dashboard


def graphs_raw(request, id):
    campaign = Campaign.objects.get(id=id)
    context = {'campaign': campaign}
    return render(request, 'graphs/graphs_raw.html', context)


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
    start_date = campaign.start_date
    end_date = campaign.end_date
    var1 = campaign.var1
    var2 = campaign.var2

    initial_data = {'start_date': start_date,
                    'end_date': end_date,
                    'var1': var1,
                    'var2': var2}

    # form
    form = DateRangeModelForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        var1 = request.POST.get('var1')
        var2 = request.POST.get('var2')

    # dataframe from range
    df = df.loc[(
        df.DATE_TIME >= np.datetime64(start_date)) & (
        df.DATE_TIME <= np.datetime64(end_date) + np.timedelta64(1, 'D'))]

    script, div = bokeh_dashboard(df, var1, var2)
    context = {'campaign': campaign,
               'form': form,
               'script': script, 'div': div}
    return render(request, 'graphs/graphs_detail.html', context)
