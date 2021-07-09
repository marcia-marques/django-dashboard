from django.urls import path

from graphs.views import graphs_list, graphs_detail

urlpatterns = [
    # path('', GraphsView.as_view(), name='graphs'),
    path('', graphs_list, name='graphs_list'),
    path('<int:id>/', graphs_detail, name='graphs_detail'),
]
