from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class PostManager(models.Manager):
    def only_public_or_author(self, user):
        if user.is_authenticated:
            user_i_follow = user.following.all()
            # showing only the posts of user i follow
            return Post.objects.all()


class Post(models.Model):
    title = models.CharField(max_length=200)  # title of the post
    # username of the author of the post
    username = models.TextField(blank=True)
    body = models.TextField(blank=True)  # body of the post
    # Store usernames as a comma-separated string
    liked = models.CharField(max_length=3000, blank=True)
    image = models.ImageField(blank=True, null=True,
                              upload_to='tweetspic')  # image of the post
    gender = models.CharField(max_length=200, blank=True)
    # iliked = models.BooleanField(default=False)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    # created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # ordering = ['-created']
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def __str__(self):
        return self.title

    @property
    def like_count(self):
        return len(self.liked.split(','))
    # def iliked(self, username):
    #     if username in self.liked.split(','):
    #         return True
    #     return False

    def add_like(self, username):
        if username not in self.liked.split(','):
            self.liked += f',{username}'
            self.save()


class Comment(models.Model):
    body = models.TextField(blank=True)  # body of the comment
    # username of the author of the comment
    username = models.TextField(blank=True)
    gender = models.CharField(max_length=200, blank=True)
    post_uuid = models.CharField(max_length=200, blank=True)
    # post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments') #post that the comment belongs to
    # date and time of the comment
    created = models.DateTimeField(auto_now_add=True)
