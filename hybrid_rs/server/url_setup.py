from typing import List

from django.urls import path, URLPattern
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from hybrid_rs.server.views.anime_views import index, anime_search, anime_description


urlpatterns: List[URLPattern] = [
    path('', index),
    path('anime', anime_search),
    path('anime/<int:anime_id>', anime_description)
] 
urlpatterns += staticfiles_urlpatterns()
