from django.urls import path
from .views import *
from .api_views import index_data_api, ranking_data_api, play_song_api, search_api

urlpatterns = [
    path("", indexView, name="index"),
    
    # API路由
    path("api/index/data/", index_data_api, name="index_data_api"),
    path("api/ranking/<str:type_name>/", ranking_data_api, name="ranking_data_api"),
    path("api/play/<int:song_id>/", play_song_api, name="play_song_api"),
    path("api/search/", search_api, name="search_api"),
]