from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    following = models.ManyToManyField(User, related_name='followers', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    verified = models.BooleanField(default=False)  # 认证标识
    total_videos = models.PositiveIntegerField(default=0)  # 总视频数
    total_views = models.PositiveIntegerField(default=0)  # 总观看数
    total_likes = models.PositiveIntegerField(default=0)  # 总点赞数
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    @property
    def follower_count(self):
        return self.followers.count()
    
    @property
    def following_count(self):
        return self.following.count()
    
    @property
    def video_count(self):
        return self.user.uploaded_videos.count()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.userprofile.save()
    except AttributeError:
        # Create profile if it doesn't exist
        UserProfile.objects.create(user=instance)


class UserFollow(models.Model):
    """
    用户关注关系模型
    """
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_relations')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_relations')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower', 'followed')
    
    def __str__(self):
        return f'{self.follower.username} follows {self.followed.username}'
