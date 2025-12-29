from django.db import models
from django.contrib.auth.models import User
from videos.models import Video


class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    is_edited = models.BooleanField(default=False)  # 是否被编辑过
    is_deleted = models.BooleanField(default=False)  # 是否被删除
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.video.title}'
    
    @property
    def total_likes(self):
        return self.comment_reactions.filter(reaction_type='like').count()
    
    @property
    def total_dislikes(self):
        return self.comment_reactions.filter(reaction_type='dislike').count()


class CommentReaction(models.Model):
    REACTION_CHOICES = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    ]
    
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('comment', 'user')
