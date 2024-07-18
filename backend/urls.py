# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('wordcloudtest.json', wordcloud_data_test, name='wordcloud_data_test'),
    path('wordcloud.json', wordcloud_data, name='wordcloud_data'),
    # other paths
    # http://localhost:8000/sdfsodfisidfd/wordcloud.json
]
