
from django.shortcuts import render

from data.models import Campaign

from .graphs import time_series


def graphs_list(request):
    campaigns = Campaign.objects.all()
    context = {'campaigns': campaigns}
    return render(request, 'graphs/graphs_list.html', context)


def graphs_detail(request, id):
    campaign = Campaign.objects.get(id=id)
    script, div = time_series(campaign)
    context = {'campaign':campaign, 'script': script, 'div': div}
    return render(request, 'graphs/graphs_detail.html', context)
