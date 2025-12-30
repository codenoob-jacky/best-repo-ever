from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import UserProfile, UserFollow, Notification


def profile(request, user_id):
    """
    用户个人资料页面（与profile_view同名函数，为URL兼容）
    """
    user = get_object_or_404(User, id=user_id)
    # 如果用户ID不匹配用户名，尝试通过用户名重定向
    return profile_view(request, user.username)


def profile_view(request, username):
    """
    用户个人资料页面
    """
    user = get_object_or_404(User, username=username)
    user_profile = user.userprofile
    
    context = {
        'profile_user': user,
        'user_profile': user_profile,
    }
    return render(request, 'users/profile.html', context)


@login_required
def edit_profile(request):
    """
    编辑个人资料页面
    """
    profile = request.user.userprofile
    
    if request.method == 'POST':
        profile.bio = request.POST.get('bio', '')
        profile.location = request.POST.get('location', '')
        profile.birth_date = request.POST.get('birth_date', None)
        
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        
        profile.save()
        return redirect('profile', username=request.user.username)
    
    context = {
        'user_profile': profile,
    }
    return render(request, 'users/edit_profile.html', context)


@login_required
def follow_user(request, user_id):
    """
    关注用户（与toggle_follow同名函数，为URL兼容）
    """
    if request.method == 'POST':
        user_to_follow = get_object_or_404(User, id=user_id)
        
        if user_to_follow == request.user:
            return JsonResponse({'success': False, 'message': 'Cannot follow yourself'})
        
        # 检查是否已经关注
        follow, created = UserFollow.objects.get_or_create(
            follower=request.user,
            followed=user_to_follow
        )
        
        if not created:  # 如果关系已存在，说明已经关注了
            return JsonResponse({
                'success': True,
                'following': True,
                'message': 'Already following',
                'follower_count': user_to_follow.userprofile.follower_count
            })
        
        return JsonResponse({
            'success': True,
            'following': True,
            'message': 'Followed successfully',
            'follower_count': user_to_follow.userprofile.follower_count
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


@login_required
def unfollow_user(request, user_id):
    """
    取消关注用户（与toggle_follow同名函数，为URL兼容）
    """
    if request.method == 'POST':
        user_to_unfollow = get_object_or_404(User, id=user_id)
        
        # 尝试删除关注关系
        try:
            follow = UserFollow.objects.get(
                follower=request.user,
                followed=user_to_unfollow
            )
            follow.delete()
            
            return JsonResponse({
                'success': True,
                'following': False,
                'message': 'Unfollowed successfully',
                'follower_count': user_to_unfollow.userprofile.follower_count
            })
        except UserFollow.DoesNotExist:
            return JsonResponse({
                'success': True,
                'following': False,
                'message': 'Not following user',
                'follower_count': user_to_unfollow.userprofile.follower_count
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


@login_required
def toggle_follow(request, user_id):
    """
    关注/取消关注用户
    """
    if request.method == 'POST':
        user_to_follow = get_object_or_404(User, id=user_id)
        
        if user_to_follow == request.user:
            return JsonResponse({'success': False, 'message': 'Cannot follow yourself'})
        
        follow, created = UserFollow.objects.get_or_create(
            follower=request.user,
            followed=user_to_follow
        )
        
        if not created:  # 如果关系已存在，删除它（取消关注）
            follow.delete()
            following = False
            message = 'Unfollowed successfully'
            
            # 删除关注通知
            Notification.objects.filter(
                recipient=user_to_follow,
                sender=request.user,
                notification_type='follow'
            ).delete()
        else:  # 如果关系不存在，创建它（关注）
            following = True
            message = 'Followed successfully'
            
            # 创建关注通知
            Notification.objects.create(
                recipient=user_to_follow,
                sender=request.user,
                notification_type='follow',
                title=f'{request.user.username} 关注了你',
                message=f'{request.user.username} 开始关注你了！',
                target_url=f'/users/profile/{request.user.id}/'
            )
        
        # 更新用户资料中的关注者计数
        followed_profile = user_to_follow.userprofile
        followed_profile.save()
        
        return JsonResponse({
            'success': True,
            'following': not created,
            'message': message,
            'follower_count': followed_profile.follower_count
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


@login_required
def notifications(request):
    """
    用户通知列表页面
    """
    notifications = request.user.notifications.all()
    
    # 标记所有通知为已读
    request.user.notifications.filter(is_read=False).update(is_read=True)
    
    context = {
        'notifications': notifications,
    }
    return render(request, 'users/notifications.html', context)


@login_required
def mark_notification_read(request, notification_id):
    """
    标记单个通知为已读
    """
    try:
        notification = request.user.notifications.get(id=notification_id, is_read=False)
        notification.mark_as_read()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Notification not found'})


@login_required
def unread_notifications_count(request):
    """
    获取未读通知数量
    """
    count = request.user.notifications.filter(is_read=False).count()
    return JsonResponse({'count': count})