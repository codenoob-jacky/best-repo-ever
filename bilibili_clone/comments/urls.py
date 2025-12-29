from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('video/<int:video_id>/', views.add_comment, name='add_comment'),
    path('<int:comment_id>/reply/', views.reply_comment, name='reply_comment'),
    path('<int:comment_id>/like/', views.like_comment, name='like_comment'),
    path('<int:comment_id>/dislike/', views.dislike_comment, name='dislike_comment'),
]