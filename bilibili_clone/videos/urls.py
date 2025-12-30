from django.urls import path
from . import views

app_name = 'videos'

urlpatterns = [
    path('', views.video_list, name='video_list'),
    path('upload/', views.video_upload, name='video_upload'),
    path('upload-new/', views.upload_video, name='upload_video'),
    path('<int:pk>/', views.video_detail, name='video_detail'),
    path('<int:pk>/like/', views.video_like, name='video_like'),
    path('<int:pk>/dislike/', views.video_dislike, name='video_dislike'),
    path('reaction/<int:video_id>/', views.toggle_video_reaction, name='toggle_video_reaction'),
    path('playlist/create/', views.create_playlist, name='create_playlist'),
    path('playlist/add/<int:video_id>/', views.add_video_to_playlist, name='add_video_to_playlist'),
    path('user/<str:username>/', views.user_videos, name='user_videos'),
]