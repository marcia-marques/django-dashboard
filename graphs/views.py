from django.shortcuts import render
import pandas as pd
import numpy as np
import glob
from datetime import datetime, timedelta

from data.models import Campaign
from .forms import (DateRangeFormFunction,
                    DataRawFormFunction, DataRaw24hFormFunction)
from .mygraphs import bokeh_dashboard, bokeh_raw


def graphs_raw_24h(request, id):
    campaign = Campaign.objects.get(id=id)

    # form choices
    path = campaign.raw_data_path
    filenames = [filename for filename in glob.iglob(
        path + '*/*/*', recursive=True)]
    if filenames:
        filenames.sort(reverse=True)
        dates = list([filename[-10:] for filename in filenames])
        date_choices = list(zip(dates, dates))

        # initial values
        days = dates[0]
        initial_data = {'days': days}

        # form
        raw_data_24h_form = DataRaw24hFormFunction(date_choices)
        form = raw_data_24h_form(request.POST or None, initial=initial_data)
        if form.is_valid():
            days = request.POST.get('days')
            if '_prev' in request.POST:
                days = (datetime.strptime(
                    days, '%Y/%m/%d') - timedelta(
                    days=1)).strftime('%Y/%m/%d')
                form = raw_data_24h_form(initial={'days': days})
            elif '_next' in request.POST:
                days = (datetime.strptime(
                    days, '%Y/%m/%d') + timedelta(
                    days=1)).strftime('%Y/%m/%d')
                form = raw_data_24h_form(initial={'days': days})

        # dataframe
        filenames = [filename for filename in glob.iglob(
            path + days + '/*', recursive=True)]
        filenames.sort()
        list_of_dfs = [pd.read_csv(filename,
                                   sep=r'\s+',
                                   engine='python',
                                   parse_dates=[['DATE', 'TIME']])
                       for filename in filenames]
        df = pd.concat(list_of_dfs, ignore_index=True)
        df['DATE_TIME'] = pd.to_datetime(df.DATE_TIME)

        script, div = bokeh_raw(df)
        context = {'campaign': campaign,
                   'form': form,
                   'script': script, 'div': div}
        return render(request, 'graphs/graphs_raw_24h.html', context)

    else:

        # form
        raw_data_24h_form = DataRaw24hFormFunction([('', 'no data available')])
        form = raw_data_24h_form(request.POST or None)
        context = {'campaign': campaign, 'form': form}
        return render(request, 'graphs/graphs_raw_24h.html', context)


def graphs_raw(request, id):
    campaign = Campaign.objects.get(id=id)

    # form choices
    path = campaign.raw_data_path
    filenames = [filename for filename in glob.iglob(
        path + '**/*.dat', recursive=True)]
    if filenames:
        filenames.sort(reverse=True)
        file_choices = list(
            zip(filenames,
                [filename.split('/')[-1] for filename in filenames]))

        # initial values
        files_name = filenames[0]
        initial_data = {'files_name': files_name}

        # form
        raw_data_form = DataRawFormFunction(file_choices)
        form = raw_data_form(request.POST or None, initial=initial_data)
        if form.is_valid():
            files_name = request.POST.get('files_name')
            idx = filenames.index(files_name)
            if '_prev' in request.POST:
                files_name = filenames[idx + 1]
                form = raw_data_form(initial={'files_name': files_name})
            elif '_next' in request.POST:
                files_name = filenames[idx - 1]
                form = raw_data_form(initial={'files_name': files_name})

        # dataframe
        df = pd.read_csv(files_name,
                         sep=r'\s+',
                         engine='python',
                         parse_dates=[['DATE', 'TIME']])
        df['DATE_TIME'] = pd.to_datetime(df.DATE_TIME)

        script, div = bokeh_raw(df)
        context = {'campaign': campaign,
                   'form': form,
                   'script': script, 'div': div}
        return render(request, 'graphs/graphs_raw.html', context)

    else:

        # form
        raw_data_form = DataRawFormFunction([('', 'no data available')])
        form = raw_data_form(request.POST or None)
        context = {'campaign': campaign, 'form': form}
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

    # form choices
    var_list = campaign.var_list.split(',')[1:]
    var_choices = list(zip(var_list, var_list))

    # form
    date_range_form = DateRangeFormFunction(var_choices, start_date, end_date)
    form = date_range_form(request.POST or None, initial=initial_data)
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
