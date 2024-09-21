
from . import views
from django.urls import path
from . import views

urlpatterns = [
    # your other URL patterns here
    path("", views.video_upload, name="empty"),
    path('upload/', views.video_upload, name='video_upload'),
    path('videos/', views.video_list, name='video_list'),
    path('videos/<int:video_id>/', views.video_detail, name='video_detail'),
    path('search/<int:video_id>/', views.search_subtitles, name='search_subtitles'),
]


