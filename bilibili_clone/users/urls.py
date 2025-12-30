from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('profile/<str:username>/', views.profile_view, name='profile_view'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('toggle-follow/<int:user_id>/', views.toggle_follow, name='toggle_follow'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/unread-count/', views.unread_notifications_count, name='unread_notifications_count'),
]