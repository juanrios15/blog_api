import os

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from users.models import CustomUser


def content_file_name(instance, filename):
    return os.path.join("gallery", filename)


class GalleryImage(models.Model):
    file_name = models.FileField(upload_to=content_file_name)

    def __str__(self):
        return str(self.file_name)


class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    images = models.ManyToManyField(GalleryImage, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    allow_comments = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    created_time = models.DateField(auto_now=False, auto_now_add=True)
    updated_time = models.DateField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    comment_text = models.CharField(max_length=250)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    previous_comment = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_time = models.DateField(auto_now=False, auto_now_add=True)
    updated_time = models.DateField(auto_now=True)

    def __str__(self):
        return self.comment_text


class Like(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    liked = models.BooleanField(default=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content = GenericForeignKey("content_type", "object_id")
    is_active = models.BooleanField(default=False)
    created_time = models.DateField(auto_now=False, auto_now_add=True)
    updated_time = models.DateField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "content_type", "object_id"], name="unique_like"),
        ]

    def __str__(self):
        return str(self.object_id)
