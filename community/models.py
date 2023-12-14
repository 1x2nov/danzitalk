from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils import timezone

class User(AbstractBaseUser):

    profile_image = models.TextField(default='default_profile.jpg')
    nickname = models.CharField(max_length=24, unique=True)

    USERNAME_FIELD = 'nickname'

    class Meta:
        db_table = 'User'

class Posting(models.Model):

    user = models.ForeignKey('User', on_delete=models.CASCADE)
    content = models.TextField()
    title = models.CharField(default='',max_length=50)
    reality = models.ForeignKey('reality.Reality', on_delete=models.CASCADE)
    hits = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    upload_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Posting'

class PostingPrefer(models.Model):

    preference = models.IntegerField(null=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="posting_prefers")
    posting = models.ForeignKey('Posting', on_delete=models.CASCADE, related_name="prefers")

    class Meta:
        db_table = 'PostingPrefer'

class Comment(models.Model):

    content = models.TextField()
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="comments")
    posting = models.ForeignKey('Posting', on_delete=models.CASCADE, related_name="comments")

    created_at = models.DateTimeField(auto_now_add=True)
    upload_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Comment'

class CommentPrefer(models.Model):

    preference = models.IntegerField(null=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="comment_prefers")
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name="prefers")

    class Meta:
        db_table = 'CommentPrefer'