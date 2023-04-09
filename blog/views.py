from django.shortcuts import render
from rest_framework import viewsets

from .models import Tag, Post, Comment, Like
from .serializers import TagSerializer, PostSerializer, CommentSerializer, LikeSerializer


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filterset_fields = {
        "name": ("exact", "icontains"),
    }


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filterset_fields = {
        "title": ("icontains",),
        "created_time": (
            "gte",
            "lte",
        ),
        "updated_time": (
            "gte",
            "lte",
        ),
        "user": ("exact",),
        "tags": ("exact", "in"),
    }


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filterset_fields = {
        "post": ("exact", "in"),
        "user": ("exact",),
        "created_time": (
            "gte",
            "lte",
        ),
        "updated_time": (
            "gte",
            "lte",
        ),
        "previous_comment": ("exact",),
    }


class LikesViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    filterset_fields = {
        "user": ("exact",),
        "created_time": (
            "gte",
            "lte",
        ),
        "updated_time": (
            "gte",
            "lte",
        ),
    }
