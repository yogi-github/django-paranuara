from django.urls import re_path, include

urlpatterns = [
    re_path(r'^info-analytics/', include(('info_analytics.urls', 'info_analytics'), namespace='info-analytics')),
]
