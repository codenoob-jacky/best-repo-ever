from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from videos.models import Video
from users.models import Notification
from .models import Comment, CommentReaction


def add_comment(request, video_id):
    """
    添加评论的视图函数
    """
    if request.method == 'POST':
        video = get_object_or_404(Video, id=video_id)
        content = request.POST.get('content')
        
        if content and request.user.is_authenticated:
            parent_id = request.POST.get('parent_id')
            parent = None
            
            if parent_id:
                try:
                    parent = Comment.objects.get(id=parent_id)
                except Comment.DoesNotExist:
                    pass
            
            comment = Comment.objects.create(
                video=video,
                author=request.user,
                content=content,
                parent=parent
            )
            
            # 如果不是回复评论，则通知视频上传者
            if not parent and video.uploader != request.user:
                Notification.objects.create(
                    recipient=video.uploader,
                    sender=request.user,
                    notification_type='comment',
                    title=f'{request.user.username} 评论了你的视频',
                    message=f'{request.user.username} 在你的视频 "{video.title}" 下发表了评论：{content[:50]}...',
                    target_url=f'{video.get_absolute_url()}#comment-{comment.id}'
                )
            
            # 如果是回复评论，通知被回复的用户（如果不是自己）
            if parent and parent.author != request.user:
                Notification.objects.create(
                    recipient=parent.author,
                    sender=request.user,
                    notification_type='comment',
                    title=f'{request.user.username} 回复了你的评论',
                    message=f'{request.user.username} 在视频 "{video.title}" 下回复了你的评论：{content[:50]}...',
                    target_url=f'{video.get_absolute_url()}#comment-{comment.id}'
                )
            
            return JsonResponse({
                'success': True,
                'message': 'Comment added successfully',
                'comment_id': comment.id
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Please log in and provide content'
            })
    
    return redirect('video_detail', pk=video_id)


@login_required
def reply_comment(request, comment_id):
    """
    回复评论的视图函数
    """
    if request.method == 'POST':
        parent_comment = get_object_or_404(Comment, id=comment_id)
        content = request.POST.get('content')
        
        if content and request.user.is_authenticated:
            reply = Comment.objects.create(
                video=parent_comment.video,
                author=request.user,
                content=content,
                parent=parent_comment
            )
            
            # 通知被回复的用户（如果不是自己）
            if parent_comment.author != request.user:
                Notification.objects.create(
                    recipient=parent_comment.author,
                    sender=request.user,
                    notification_type='comment',
                    title=f'{request.user.username} 回复了你的评论',
                    message=f'{request.user.username} 在视频 "{parent_comment.video.title}" 下回复了你的评论：{content[:50]}...',
                    target_url=f'{parent_comment.video.get_absolute_url()}#comment-{reply.id}'
                )
            
            return JsonResponse({
                'success': True,
                'message': 'Reply added successfully',
                'comment_id': reply.id
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Please log in and provide content'
            })
    
    return redirect('video_detail', pk=parent_comment.video.pk)


@login_required
def like_comment(request, comment_id):
    """
    点赞评论的视图函数
    """
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        
        # 检查是否存在已有反应
        existing_reaction = CommentReaction.objects.filter(
            comment=comment,
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
            CommentReaction.objects.create(
                comment=comment,
                user=request.user,
                reaction_type='like'
            )
            
            # 通知评论作者（如果不是自己）
            if comment.author != request.user:
                Notification.objects.create(
                    recipient=comment.author,
                    sender=request.user,
                    notification_type='like',
                    title=f'{request.user.username} 点赞了你的评论',
                    message=f'{request.user.username} 点赞了你在视频 "{comment.video.title}" 下的评论',
                    target_url=f'{comment.video.get_absolute_url()}#comment-{comment.id}'
                )
        
        # 返回更新后的统计信息
        return JsonResponse({
            'success': True,
            'likes': comment.total_likes,
            'dislikes': comment.total_dislikes
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


@login_required
def dislike_comment(request, comment_id):
    """
    点踩评论的视图函数
    """
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        
        # 检查是否存在已有反应
        existing_reaction = CommentReaction.objects.filter(
            comment=comment,
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
            CommentReaction.objects.create(
                comment=comment,
                user=request.user,
                reaction_type='dislike'
            )
        
        # 返回更新后的统计信息
        return JsonResponse({
            'success': True,
            'likes': comment.total_likes,
            'dislikes': comment.total_dislikes
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


@login_required
def delete_comment(request, comment_id):
    """
    删除评论的视图函数
    """
    comment = get_object_or_404(Comment, id=comment_id)
    
    # 检查用户权限
    if comment.author == request.user or comment.video.uploader == request.user:
        comment.is_deleted = True
        comment.save()
        return JsonResponse({'success': True, 'message': 'Comment deleted'})
    else:
        return JsonResponse({'success': False, 'message': 'Permission denied'})


@login_required
def toggle_comment_reaction(request, comment_id):
    """
    切换评论点赞/点踩的视图函数
    """
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        reaction_type = request.POST.get('reaction_type')
        
        if reaction_type not in ['like', 'dislike']:
            return JsonResponse({'success': False, 'message': 'Invalid reaction type'})
        
        # 检查是否存在已有反应
        existing_reaction = CommentReaction.objects.filter(
            comment=comment,
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
            CommentReaction.objects.create(
                comment=comment,
                user=request.user,
                reaction_type=reaction_type
            )
        
        # 返回更新后的统计信息
        return JsonResponse({
            'success': True,
            'likes': comment.total_likes,
            'dislikes': comment.total_dislikes
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})