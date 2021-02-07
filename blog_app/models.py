from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class PostCategory(models.Model):
    class Meta:
        db_table = 't_post_categories'
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25, unique=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} (Id: {})'.format(self.name, self.id)


class Post(models.Model):
    class Meta:
        db_table = 't_posts'
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey('PostCategory', related_name='posts', null=False, blank=False, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(get_user_model(), null=False, blank=False, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100, blank=False, null=False)
    content = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} | Author: {} | (Id: {})'.format(self.title, self.author, self.id)


class PostComment(models.Model):
    class Meta:
        db_table = 't_post_comments'
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey('Post', related_name='comments', null=False, blank=False, on_delete=models.CASCADE)
    commenter = models.ForeignKey(get_user_model(), null=False, blank=False, on_delete=models.DO_NOTHING)
    content = models.CharField(max_length=250, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} (Id: {})'.format(self.content, self.id)

