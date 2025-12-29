from django.urls import path
from . import views

app_name = 'videos'

urlpatterns = [
    path('', views.video_list, name='video_list'),
    path('upload/', views.video_upload, name='video_upload'),
    path('<int:pk>/', views.video_detail, name='video_detail'),
    path('<int:pk>/like/', views.video_like, name='video_like'),
    path('<int:pk>/dislike/', views.video_dislike, name='video_dislike'),
]