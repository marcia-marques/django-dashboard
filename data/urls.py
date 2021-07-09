from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import CampaignListView

urlpatterns = [
    path('', CampaignListView.as_view(), name='campaign_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
