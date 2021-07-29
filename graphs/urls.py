from django.urls import path

from graphs.views import graphs_list, graphs_detail, graphs_raw, graphs_raw_24h

urlpatterns = [
    # path('', GraphsView.as_view(), name='graphs'),
    path('', graphs_list, name='graphs_list'),
    path('<int:id>/', graphs_detail, name='graphs_detail'),
    path('raw/<int:id>/', graphs_raw, name='graphs_raw'),
    path('raw-24h/<int:id>/', graphs_raw_24h, name='graphs_raw_24h'),
]
