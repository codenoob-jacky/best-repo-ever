from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Video, VideoCategory, VideoTag


def video_list(request):
    videos = Video.objects.all()
    categories = VideoCategory.objects.all()
    tags = VideoTag.objects.all()
    
    context = {
        'videos': videos,
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'videos/video_list.html', context)


def video_detail(request, pk):
    video = get_object_or_404(Video, pk=pk)
    # 增加观看次数
    video.views += 1
    video.save()
    
    context = {
        'video': video,
    }
    return render(request, 'videos/video_detail.html', context)


@login_required
def video_upload(request):
    if request.method == 'POST':
        # 处理视频上传
        title = request.POST.get('title')
        description = request.POST.get('description')
        video_file = request.FILES.get('video_file')
        thumbnail = request.FILES.get('thumbnail')
        
        video = Video.objects.create(
            title=title,
            description=request.POST.get('description'),
            video_file=video_file,
            thumbnail=thumbnail,
            uploader=request.user
        )
        
        return redirect('videos:video_detail', pk=video.pk)
    else:
        # 显示上传表单
        categories = VideoCategory.objects.all()
        tags = VideoTag.objects.all()
        
        context = {
            'categories': categories,
            'tags': tags,
        }
        return render(request, 'videos/upload.html', context)


@require_POST
@login_required
def video_like(request, pk):
    video = get_object_or_404(Video, pk=pk)
    video.likes += 1
    video.save()
    
    return JsonResponse({'likes': video.likes})


@require_POST
@login_required
def video_dislike(request, pk):
    video = get_object_or_404(Video, pk=pk)
    video.dislikes += 1
    video.save()
    
    return JsonResponse({'dislikes': video.dislikes})
