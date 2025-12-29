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
    
    class Meta:
        ordering = ['-upload_date']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('video_detail', kwargs={'pk': self.pk})


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
