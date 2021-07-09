# from django.shortcuts import render
from django.views.generic import ListView

from .models import Campaign


class CampaignListView(ListView):
    model = Campaign
    template_name = 'data/campaign_list.html'
    context_object_name = 'campaigns'
