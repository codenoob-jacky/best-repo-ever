from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q, Max
from .models import Video, VideoCategory, VideoTag, VideoReaction, VideoView, Playlist, PlaylistItem
from comments.models import Comment
from users.models import Notification


def video_list(request):
    """
    视频列表页面
    """
    videos = Video.objects.filter(published=True).select_related('uploader').prefetch_related('video_reactions')
    categories = VideoCategory.objects.all()
    
    # 获取搜索查询
    query = request.GET.get('q')
    if query:
        videos = videos.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) | 
            Q(uploader__username__icontains=query)
        )
    
    # 获取分类过滤
    category_id = request.GET.get('category')
    if category_id:
        videos = videos.filter(videocategoryrelation__category_id=category_id)
    
    context = {
        'videos': videos,
        'categories': categories,
        'query': query,
        'selected_category': int(category_id) if category_id else None
    }
    return render(request, 'videos/video_list.html', context)


def video_detail(request, pk):
    """
    视频详情页面
    """
    video = get_object_or_404(Video, pk=pk, published=True)
    
    # 增加观看次数
    if request.user.is_authenticated:
        # 检查是否已经观看过
        if not VideoView.objects.filter(video=video, user=request.user).exists():
            VideoView.objects.create(video=video, user=request.user)
            video.view_count += 1
            video.save()
    else:
        # 对于未登录用户，使用IP地址追踪
        ip_address = request.META.get('REMOTE_ADDR')
        if not VideoView.objects.filter(video=video, ip_address=ip_address).exists():
            VideoView.objects.create(video=video, ip_address=ip_address)
            video.view_count += 1
            video.save()
    
    # 获取视频的评论
    comments = Comment.objects.filter(video=video, parent=None, is_deleted=False).select_related('author')
    
    # 获取相关视频（基于分类的推荐）
    related_videos = Video.objects.filter(
        videocategoryrelation__category__in=video.videocategoryrelation_set.values('category')
    ).exclude(pk=pk).distinct()[:6]
    
    # 如果基于分类的推荐不够，添加热门视频
    if related_videos.count() < 6:
        additional_videos = Video.objects.exclude(
            pk=pk, 
            pk__in=[v.pk for v in related_videos]
        ).order_by('-view_count')[:6 - related_videos.count()]
        related_videos = list(related_videos) + list(additional_videos)
    
    context = {
        'video': video,
        'comments': comments,
        'related_videos': related_videos,
    }
    return render(request, 'videos/video_detail.html', context)


@login_required
def video_upload(request):
    """
    上传视频页面（与upload_video同名函数，为URL兼容）
    """
    return upload_video(request)


@login_required
def upload_video(request):
    """
    上传视频页面
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        video_file = request.FILES.get('video_file')
        thumbnail = request.FILES.get('thumbnail')
        
        if title and video_file:
            video = Video.objects.create(
                title=title,
                description=description,
                video_file=video_file,
                thumbnail=thumbnail,
                uploader=request.user
            )
            
            # 处理分类
            category_ids = request.POST.getlist('categories')
            for cat_id in category_ids:
                try:
                    category = VideoCategory.objects.get(id=cat_id)
                    video.videocategoryrelation_set.create(category=category)
                except VideoCategory.DoesNotExist:
                    pass
            
            # 处理标签
            tags = request.POST.get('tags', '').split(',')
            for tag_name in tags:
                tag_name = tag_name.strip()
                if tag_name:
                    tag, created = VideoTag.objects.get_or_create(name=tag_name)
                    video.videotagrelation_set.create(tag=tag)
            
            return redirect('video_detail', pk=video.pk)
    
    categories = VideoCategory.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'videos/upload.html', context)


@login_required
def video_like(request, pk):
    """
    视频点赞（为URL兼容）
    """
    if request.method == 'POST':
        video = get_object_or_404(Video, id=pk)
        
        # 检查是否存在已有反应
        existing_reaction = VideoReaction.objects.filter(
            video=video,
            user=request.user
        ).first()
        
        if existing_reaction:
            if existing_reaction.reaction_type == 'like':
                # 如果已经是点赞，则取消
                existing_reaction.delete()
            else:
                # 如果是点踩，则改为点赞
                existing_reaction.reaction_type = 'like'
                existing_reaction.save()
        else:
            # 创建新的点赞
            VideoReaction.objects.create(
                video=video,
                user=request.user,
                reaction_type='like'
            )
            
            # 通知视频上传者（如果不是自己）
            if video.uploader != request.user:
                Notification.objects.create(
                    recipient=video.uploader,
                    sender=request.user,
                    notification_type='like',
                    title=f'{request.user.username} 点赞了你的视频',
                    message=f'{request.user.username} 点赞了你的视频 "{video.title}"',
                    target_url=f'{video.get_absolute_url()}'
                )
        
        # 返回更新后的统计信息
        return JsonResponse({
            'success': True,
            'likes': video.total_likes,
            'dislikes': video.total_dislikes
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


@login_required
def video_dislike(request, pk):
    """
    视频点踩（为URL兼容）
    """
    if request.method == 'POST':
        video = get_object_or_404(Video, id=pk)
        
        # 检查是否存在已有反应
        existing_reaction = VideoReaction.objects.filter(
            video=video,
            user=request.user
        ).first()
        
        if existing_reaction:
            if existing_reaction.reaction_type == 'dislike':
                # 如果已经是点踩，则取消
                existing_reaction.delete()
            else:
                # 如果是点赞，则改为点踩
                existing_reaction.reaction_type = 'dislike'
                existing_reaction.save()
        else:
            # 创建新的点踩
            VideoReaction.objects.create(
                video=video,
                user=request.user,
                reaction_type='dislike'
            )
        
        # 返回更新后的统计信息
        return JsonResponse({
            'success': True,
            'likes': video.total_likes,
            'dislikes': video.total_dislikes
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


@login_required
def toggle_video_reaction(request, video_id):
    """
    切换视频点赞/点踩
    """
    if request.method == 'POST':
        video = get_object_or_404(Video, id=video_id)
        reaction_type = request.POST.get('reaction_type')
        
        if reaction_type not in ['like', 'dislike']:
            return JsonResponse({'success': False, 'message': 'Invalid reaction type'})
        
        # 检查是否存在已有反应
        existing_reaction = VideoReaction.objects.filter(
            video=video,
            user=request.user
        ).first()
        
        if existing_reaction:
            if existing_reaction.reaction_type == reaction_type:
                # 如果是相同的反应类型，则删除
                existing_reaction.delete()
            else:
                # 如果是不同的反应类型，则更新
                existing_reaction.reaction_type = reaction_type
                existing_reaction.save()
        else:
            # 创建新的反应
            VideoReaction.objects.create(
                video=video,
                user=request.user,
                reaction_type=reaction_type
            )
        
        # 返回更新后的统计信息
        return JsonResponse({
            'success': True,
            'likes': video.total_likes,
            'dislikes': video.total_dislikes
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


@login_required
def create_playlist(request):
    """
    创建播放列表
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        is_public = request.POST.get('is_public', 'on') == 'on'
        
        playlist = Playlist.objects.create(
            name=name,
            description=description,
            owner=request.user,
            is_public=is_public
        )
        
        return JsonResponse({
            'success': True,
            'playlist_id': playlist.id,
            'message': 'Playlist created successfully'
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


@login_required
def add_video_to_playlist(request, video_id):
    """
    将视频添加到播放列表
    """
    if request.method == 'POST':
        video = get_object_or_404(Video, id=video_id)
        playlist_id = request.POST.get('playlist_id')
        
        playlist = get_object_or_404(Playlist, id=playlist_id, owner=request.user)
        
        # 找到下一个位置
        max_position = playlist.items.aggregate(max_pos=Max('position'))['max_pos'] or 0
        position = max_position + 1
        
        PlaylistItem.objects.get_or_create(
            playlist=playlist,
            video=video,
            defaults={'position': position}
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Video added to playlist'
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def user_videos(request, username):
    """
    用户上传的视频列表
    """
    user = get_object_or_404(User, username=username)
    videos = Video.objects.filter(uploader=user, published=True).select_related('uploader')
    
    context = {
        'profile_user': user,
        'videos': videos,
    }
    return render(request, 'videos/user_videos.html', context)