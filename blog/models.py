from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from users.models import CustomUser


class Image(models.Model):
    file_name = models.FileField(upload_to=None)

    def __str__(self):
        return str(self.file_name)


class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_time = models.DateField(auto_now=False, auto_now_add=True)
    updated_time = models.DateField(auto_now=True, auto_now_add=True)
    images = models.ForeignKey(Image, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    allow_comments = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    comment = models.CharField(max_length=250)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_time = models.DateField(auto_now=False, auto_now_add=True)
    updated_time = models.DateField(auto_now=True, auto_now_add=True)
    previous_comment = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.comment


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    liked = models.BooleanField(default=True)
    created_time = models.DateField(auto_now=False, auto_now_add=True)
    updated_time = models.DateField(auto_now=True, auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return str(self.object_id)
