from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_videos')
    upload_date = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    duration = models.DurationField(null=True, blank=True)  # 视频时长
    published = models.BooleanField(default=True)  # 是否发布
    view_count = models.PositiveIntegerField(default=0)  # 观看次数
    like_count = models.PositiveIntegerField(default=0)  # 点赞数
    dislike_count = models.PositiveIntegerField(default=0)  # 点踩数
    comment_count = models.PositiveIntegerField(default=0)  # 评论数
    
    class Meta:
        ordering = ['-upload_date']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('video_detail', kwargs={'pk': self.pk})
    
    @property
    def total_likes(self):
        return self.video_reactions.filter(reaction_type='like').count()
    
    @property
    def total_dislikes(self):
        return self.video_reactions.filter(reaction_type='dislike').count()


class VideoCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name


class VideoTag(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


class VideoCategoryRelation(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    category = models.ForeignKey(VideoCategory, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('video', 'category')


class VideoTagRelation(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    tag = models.ForeignKey(VideoTag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('video', 'tag')


class VideoReaction(models.Model):
    """
    视频点赞/点踩模型
    """
    REACTION_CHOICES = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    ]
    
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='video_reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('video', 'user')


class VideoView(models.Model):
    """
    视频观看记录模型
    """
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='video_views')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    
    class Meta:
        unique_together = ('video', 'user', 'session_key', 'ip_address')


class Playlist(models.Model):
    """
    播放列表模型
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


class PlaylistItem(models.Model):
    """
    播放列表项目模型
    """
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='items')
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    position = models.PositiveIntegerField()
    
    class Meta:
        unique_together = ('playlist', 'position')
        ordering = ['position']
