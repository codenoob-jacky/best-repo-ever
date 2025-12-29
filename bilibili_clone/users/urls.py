from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
]