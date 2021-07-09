from django.urls import path

from graphs.views import GraphsView

urlpatterns = [
    path('', GraphsView.as_view(), name='graphs'),
]
