
from django.urls import path, include
from streaming import views


urlpatterns = [
    path('', views.index, name='index'),
    path('event', views.event, name='Event'),
    path('VideoCamera_feed', views.VideoCamera_feed, name='VideoCamera_feed'),
	path('LiveWebCam_feed', views.LiveWebCam_feed, name='LiveWebCam_feed'),
	path('videorecordinframe_feed', views.videorecordinframe_feed, name='videorecordinframe_feed'),
	path('record_audio', views.record_audio, name='record_audio'),
	path('VideoCamera_Event', views.VideoCamera_Event, name='VideoCamera_Event'),
    ]

