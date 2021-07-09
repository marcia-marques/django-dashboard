# from django.shortcuts import render
from django.views.generic import TemplateView


class GraphsView(TemplateView):
    template_name = 'graphs/graphs.html'
